from app.common.helpers import address_to_bytea
import pytest
import datetime
from unittest.mock import AsyncMock, MagicMock
import sqlalchemy as sa
from app.common.schemas import MAX_LIMIT

from app.wallet.models import WalletAttributes
from app.nft_holders.models import NftHolders
from app.audience.repository import AudienceRepository
from app.audience.schemas import (
    AudienceItem,
    GetAudienceAggregationRequest,
    GetAudienceAggregationResponse,
    GetAudienceRequest,
)


def coalesce(field: sa.Column) -> sa.Column:
    ifnull_value = 0
    if field.type.python_type == datetime.datetime:
        ifnull_value = datetime.datetime.fromtimestamp(0)
    return sa.func.coalesce(field, ifnull_value).label(field.name)


@pytest.fixture()
def session():
    class AsyncMockSessionMaker:
        s = AsyncMock()

        async def __aenter__(self, *args, **kwargs):
            return self.s

        async def __aexit__(self, *args, **kwargs):
            pass

    return AsyncMockSessionMaker


@pytest.fixture()
def repository(session):
    return AudienceRepository(session)


@pytest.fixture()
def audience_row():
    mocked_row = MagicMock()
    mocked_row.WalletAttributes = WalletAttributes(
        wallet='0x1',
        created_at=datetime.datetime.fromtimestamp(42),
        ens_name='foo.eth',
        labels=['aaa', 'bbb'],
        nfts_count=5,
        twitter_avatar_url='https://twitter.com/avatar',
        twitter_followers_count=4,
        twitter_url='https://twitter.com/foo',
        twitter_username='foo',
        tx_count=3,
        last_month_tx_count=2,
        last_month_in_volume=2,
        last_month_out_volume=3,
        last_month_volume=5,
        wallet_usd_cap=1,
        whitelist_activity=['0xC'],
        superrank=99,
    )
    return mocked_row


@pytest.mark.asyncio
async def test_audience_mapping(repository, audience_row):
    repository.session.s.execute.return_value = [audience_row]

    request = GetAudienceRequest(audience_name='foo')
    items, has_more = await repository.fetch_audience(request)

    assert len(items) == 1
    assert not has_more
    assert items[0] == AudienceItem(
        score_id='0',
        score=0,
        wallet=audience_row.WalletAttributes.wallet,
        superrank=audience_row.WalletAttributes.superrank,
        created_at=audience_row.WalletAttributes.created_at.timestamp(),
        ens_name=audience_row.WalletAttributes.ens_name,
        labels=audience_row.WalletAttributes.labels,
        nfts_count=audience_row.WalletAttributes.nfts_count,
        twitter_avatar_url=audience_row.WalletAttributes.twitter_avatar_url,
        twitter_followers_count=audience_row.WalletAttributes.twitter_followers_count,
        twitter_url=audience_row.WalletAttributes.twitter_url,
        twitter_username=audience_row.WalletAttributes.twitter_username,
        tx_count=audience_row.WalletAttributes.tx_count,
        last_month_tx_count=audience_row.WalletAttributes.last_month_tx_count,
        last_month_in_volume=audience_row.WalletAttributes.last_month_in_volume,
        last_month_out_volume=audience_row.WalletAttributes.last_month_out_volume,
        last_month_volume=audience_row.WalletAttributes.last_month_volume,
        wallet_usd_cap=audience_row.WalletAttributes.wallet_usd_cap,
        whitelist_activity=audience_row.WalletAttributes.whitelist_activity,
    )


common_audience_query = (
    sa.select(WalletAttributes)
)

common_total_count_query = (
    sa.select(sa.func.count(WalletAttributes.wallet_b))
)


def expected_overlap_subquery(prefix: str, contract: str) -> sa.Select:
    return sa.select(address_to_bytea(NftHolders.wallet)).where(
        sa.and_(
            NftHolders.contract_prefix == prefix, NftHolders.token_contract == contract
        )
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'request_, expected_sql',
    [
        (
            GetAudienceRequest(
                audience_name='foo',
                limit=10,
                offset=10,
            ),
            str(
                common_total_count_query.where(WalletAttributes.labels.contains(['foo'])).compile(
                    compile_kwargs={"literal_binds": True}
                )
            ),
        ),
        (
            GetAudienceRequest(
                audience_name='foo',
                order_by_field='score',
                order_by_direction='DESC',
                where_field='labels',
                where_operator='contains',
                where_values=['aaa', 'bbb', 'ccc'],
                search='0xDEAD',
                limit=10,
                offset=10,
            ),
            str(
                common_total_count_query.where(
                    WalletAttributes.labels.contains(['foo']),
                    WalletAttributes.labels.contains(['aaa', 'bbb', 'ccc']),
                    sa.or_(
                        sa.func.lower(WalletAttributes.ens_name).contains(
                            '0xDEAD'.lower()
                        ),
                        sa.func.lower(WalletAttributes.wallet).contains('0xDEAD'.lower()),
                        # temporarily disabled because of performance issues
                        # sa.func.lower(WalletAttributes.twitter_username).contains(
                        #     '0xDEAD'.lower()
                        # ),
                    ),
                ).compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetAudienceRequest(
                audience_name='bar',
                overlap_audiences=[
                    '0x0000000000000000000000000000000000000000',
                    '-0x1000000000000000000000000000000000000000',
                    '0xDEAD',  # wrong address should be ignored
                ],
            ),
            str(
                common_total_count_query.where(
                    WalletAttributes.wallet_b.in_(
                        expected_overlap_subquery(
                            '0x0', '0x0000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(
                    WalletAttributes.wallet_b.notin_(
                        expected_overlap_subquery(
                            '0x1', '0x1000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(WalletAttributes.labels.contains(['bar']),)
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
    ],
)
async def test_fetch_audience_count(repository, request_, expected_sql):
    repository.session.s.scalar.return_value = 42

    res = await repository.fetch_audience_count(request_)

    assert repository.session.s.scalar.call_count == 1
    total_count_actual_sql = str(
        repository.session.s.scalar.call_args[0][0].compile(
            compile_kwargs={"literal_binds": True}
        )
    )

    assert total_count_actual_sql == expected_sql
    assert res == 42


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'request_, expected_audience_sql',
    [
        (
            GetAudienceRequest(
                audience_name='foo',
                order_by_fields=['superrank'],
                order_by_direction='DESC',
                where_field='labels',
                where_operator='contains',
                where_values=['aaa', 'bbb', 'ccc'],
                search='0xDEAD',
                limit=9,
                offset=1,
            ),
            str(
                common_audience_query.where(
                    WalletAttributes.labels.contains(['foo']),
                    WalletAttributes.labels.contains(['aaa', 'bbb', 'ccc']),
                    sa.or_(
                        sa.func.lower(WalletAttributes.ens_name).contains(
                            '0xDEAD'.lower()
                        ),
                        sa.func.lower(WalletAttributes.wallet).contains('0xDEAD'.lower()),
                        # temporarily disabled because of performance issues
                        # sa.func.lower(WalletAttributes.twitter_username).contains(
                        #     '0xDEAD'.lower()
                        # ),
                    ),
                )
                .order_by(
                    sa.desc(WalletAttributes.superrank).nulls_last(),
                    WalletAttributes.wallet_b.asc(),
                )
                .limit(9 + 1)
                .offset(1)
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetAudienceRequest(
                audience_name='bar',
                where_field='tx_count',
                where_operator='eq',
                where_values=['10'],
            ),
            str(
                common_audience_query.where(
                    WalletAttributes.labels.contains(['bar']),
                    WalletAttributes.tx_count == 10,
                )
                .order_by(WalletAttributes.wallet_b.asc())
                .limit(MAX_LIMIT + 1)
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetAudienceRequest(
                audience_name='bar',
                where_field='ens_name',
                where_operator='ne',
                where_values=['black.eth'],
            ),
            str(
                common_audience_query.where(
                    WalletAttributes.labels.contains(['bar']),
                    WalletAttributes.ens_name != 'black.eth',
                )
                .order_by(WalletAttributes.wallet_b.asc())
                .limit(MAX_LIMIT + 1)
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetAudienceRequest(
                audience_name='bar',
                where_field='labels',
                where_operator='overlap',
                where_values=['aaa', 'bbb', 'ccc'],
            ),
            str(
                common_audience_query.where(
                    WalletAttributes.labels.contains(['bar']),
                    WalletAttributes.labels.bool_op('&&')(['aaa', 'bbb', 'ccc']),
                )
                .order_by(WalletAttributes.wallet_b.asc())
                .limit(MAX_LIMIT + 1)
                .compile(compile_kwargs={"literal_binds": True})
            )
        ),
        (
            GetAudienceRequest(
                audience_name='bar',
                overlap_audiences=[
                    '0x0000000000000000000000000000000000000000',
                    '-0x1000000000000000000000000000000000000000',
                    '0xDEAD',  # wrong address should be ignored
                ],
            ),
            str(
                common_audience_query.where(
                    WalletAttributes.wallet_b.in_(
                        expected_overlap_subquery(
                            '0x0', '0x0000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(
                    WalletAttributes.wallet_b.notin_(
                        expected_overlap_subquery(
                            '0x1', '0x1000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(WalletAttributes.labels.contains(['bar']),)
                .order_by(sa.asc(WalletAttributes.wallet_b))
                .limit(MAX_LIMIT + 1)
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
    ],
)
async def test_fetch_audience(
    repository, audience_row, request_, expected_audience_sql
):
    repository.session.s.execute.return_value = [audience_row]

    await repository.fetch_audience(request_)

    # Check that the audience query is built correctly
    assert repository.session.s.execute.call_count == 1
    audience_actual_sql = str(
        repository.session.s.execute.call_args[0][0].compile(
            compile_kwargs={"literal_binds": True}
        )
    )
    assert audience_actual_sql == expected_audience_sql


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query_result, expected_result",
    [
        (
            MagicMock(
                mappings=MagicMock(
                    return_value=MagicMock(first=MagicMock(return_value={"count": 42}))
                )
            ),
            GetAudienceAggregationResponse(values=[42]),
        ),
        (
            MagicMock(
                mappings=MagicMock(
                    return_value=MagicMock(
                        first=MagicMock(return_value={"c3": 42, "c1": 10, "c2": 500})
                    )
                )
            ),
            GetAudienceAggregationResponse(values=[42, 10, 500]),
        ),
    ],
)
async def test_audience_aggregate_mapping(repository, query_result, expected_result):
    repository.session.s.execute.return_value = query_result

    result = await repository.fetch_audience_aggregation(
        GetAudienceAggregationRequest(
            audience_name="foo", agg_type="count", agg_field="wallet"
        )
    )

    assert result == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_, expected_sql",
    [
        # simple agg functions
        (
            GetAudienceAggregationRequest(
                audience_name="foo",
                agg_type="count",
                agg_field="twitter_url",
                where_field="twitter_url",
                where_values=[None],
                where_operator="ne",
                search="0xDEAD",
            ),
            str(
                sa.select(sa.func.count(WalletAttributes.twitter_url))
                .where(
                    WalletAttributes.labels.contains(['foo']),
                    WalletAttributes.twitter_url != None,
                )
                .where(
                    sa.or_(
                        sa.func.lower(WalletAttributes.ens_name).contains(
                            '0xDEAD'.lower()
                        ),
                        sa.func.lower(WalletAttributes.wallet).contains('0xDEAD'.lower()),
                        # temporarily disabled because of performance issues
                        # sa.func.lower(WalletAttributes.twitter_username).contains(
                        #     '0xDEAD'.lower()
                        # ),
                    )
                )
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetAudienceAggregationRequest(
                audience_name="bar",
                agg_type="sum",
                agg_field="wallet_usd_cap",
                where_field="wallet_usd_cap",
            ),
            str(
                sa.select(sa.func.sum(WalletAttributes.wallet_usd_cap))
                .where(
                    WalletAttributes.labels.contains(['bar']),
                )
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        # agg functions with bucket interval
        (
            GetAudienceAggregationRequest(
                audience_name="foo",
                agg_type="count_bucket_intervals",
                agg_field="wallet_usd_cap",
                buckets=["t:99", "f:100;t:999", "f:1000"],
            ),
            str(
                sa.select(
                    sa.func.count(
                        coalesce(WalletAttributes.wallet_usd_cap)
                    ).filter(
                        coalesce(WalletAttributes.wallet_usd_cap) <= 99
                    ),
                    sa.func.count(coalesce(WalletAttributes.wallet_usd_cap))
                    .filter(coalesce(WalletAttributes.wallet_usd_cap) >= 100)
                    .filter(
                        coalesce(WalletAttributes.wallet_usd_cap) <= 999
                    ),
                    sa.func.count(coalesce(WalletAttributes.wallet_usd_cap))
                    .filter(
                        coalesce(WalletAttributes.wallet_usd_cap) >= 1000
                    ),
                )
                .where(
                    WalletAttributes.labels.contains(['foo']),
                )
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetAudienceAggregationRequest(
                audience_name="foo",
                agg_type="count_bucket_intervals",
                agg_field="created_at",
                buckets=["t:99", "f:100;t:999", "f:1000"],
            ),
            str(
                sa.select(
                    sa.func.count(
                        coalesce(WalletAttributes.created_at)
                    ).filter(
                        coalesce(WalletAttributes.created_at) <= datetime.datetime.fromtimestamp(99)
                    ),
                    sa.func.count(coalesce(WalletAttributes.created_at))
                    .filter(coalesce(WalletAttributes.created_at) >= datetime.datetime.fromtimestamp(100))
                    .filter(
                        coalesce(WalletAttributes.created_at) <= datetime.datetime.fromtimestamp(999)
                    ),
                    sa.func.count(coalesce(WalletAttributes.created_at))
                    .filter(
                        coalesce(WalletAttributes.created_at) >= datetime.datetime.fromtimestamp(1000)
                    ),
                )
                .where(
                    WalletAttributes.labels.contains(['foo']),
                )
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        # agg functions with bucket values
        (
            GetAudienceAggregationRequest(
                audience_name="foo",
                agg_type="count_bucket_values",
                agg_field="labels",
                buckets=["a", "b", "c"],
            ),
            str(
                sa.select(
                    sa.func.count(WalletAttributes.labels).filter(
                        WalletAttributes.labels.contains(['a'])
                    ),
                    sa.func.count(WalletAttributes.labels).filter(
                        WalletAttributes.labels.contains(['b'])
                    ),
                    sa.func.count(WalletAttributes.labels).filter(
                        WalletAttributes.labels.contains(['c'])
                    ),
                )
                .where(
                    WalletAttributes.labels.contains(['foo']),
                )
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        # overlapped audience
        (
            GetAudienceAggregationRequest(
                audience_name="bar",
                agg_type="sum",
                agg_field="wallet_usd_cap",
                where_field="wallet_usd_cap",
                overlap_audiences=[
                    '0x0000000000000000000000000000000000000000',
                    '-0x1000000000000000000000000000000000000000',
                    '0xDEAD',  # wrong address should be ignored
                ],
            ),
            str(
                sa.select(sa.func.sum(WalletAttributes.wallet_usd_cap))
                .where(
                    WalletAttributes.labels.contains(['bar']),
                )
                .where(
                    WalletAttributes.wallet_b.in_(
                        expected_overlap_subquery(
                            '0x0', '0x0000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(
                    WalletAttributes.wallet_b.notin_(
                        expected_overlap_subquery(
                            '0x1', '0x1000000000000000000000000000000000000000'
                        )
                    )
                )
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
    ],
)
async def test_fetch_audience_aggregation(repository, request_, expected_sql):
    mocked_result = MagicMock()
    mocked_result.mappings.first.return_value = {'count': 42}
    repository.session.s.execute.return_value = mocked_result

    await repository.fetch_audience_aggregation(request_)

    # Check that the aggregation query is built correctly
    assert repository.session.s.execute.call_count == 1
    actual_sql = str(
        repository.session.s.execute.call_args[0][0].compile(
            compile_kwargs={"literal_binds": True}
        )
    )
    assert actual_sql == expected_sql
