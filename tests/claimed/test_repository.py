from app.common.helpers import address_to_bytea
import pytest
import datetime
from unittest.mock import AsyncMock, MagicMock
import sqlalchemy as sa
from app.common.enums import BlockchainType
from app.common.schemas import MAX_LIMIT

from app.wallet.models import WalletAttributes
from app.claimed.models import Claimed
from app.nft_holders.models import NftHolders
from app.claimed.repository import ClaimedRepository
from app.claimed.schemas import (
    ClaimedItem,
    GetClaimedAggregationRequest,
    GetClaimedAggregationResponse,
    GetClaimedRequest,
)


def coalesce(field: sa.Column) -> sa.Column:
    return sa.func.coalesce(field, 0).label(field.name)


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
    return ClaimedRepository(session)


@pytest.fixture()
def claimed_row():
    mocked_row = MagicMock()
    mocked_row.Claimed = Claimed(
        wallet='0x1',
        blockchain=BlockchainType.POLYGON,
        claimed_contract='0xC',
    )
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
async def test_claimed_mapping(repository, claimed_row):
    repository.session.s.execute.return_value = [claimed_row]

    request = GetClaimedRequest(claimed_contract='0xC')
    items, has_more = await repository.fetch_claimed(request)

    assert len(items) == 1
    assert not has_more
    assert items[0] == ClaimedItem(
        wallet=claimed_row.Claimed.wallet,
        blockchain=claimed_row.Claimed.blockchain,
        claimed_contract=claimed_row.Claimed.claimed_contract,
        claimed_at=1,
        superrank=claimed_row.WalletAttributes.superrank,
        created_at=claimed_row.WalletAttributes.created_at.timestamp(),
        ens_name=claimed_row.WalletAttributes.ens_name,
        labels=claimed_row.WalletAttributes.labels,
        nfts_count=claimed_row.WalletAttributes.nfts_count,
        twitter_avatar_url=claimed_row.WalletAttributes.twitter_avatar_url,
        twitter_followers_count=claimed_row.WalletAttributes.twitter_followers_count,
        twitter_url=claimed_row.WalletAttributes.twitter_url,
        twitter_username=claimed_row.WalletAttributes.twitter_username,
        tx_count=claimed_row.WalletAttributes.tx_count,
        last_month_tx_count=claimed_row.WalletAttributes.last_month_tx_count,
        last_month_in_volume=claimed_row.WalletAttributes.last_month_in_volume,
        last_month_out_volume=claimed_row.WalletAttributes.last_month_out_volume,
        last_month_volume=claimed_row.WalletAttributes.last_month_volume,
        wallet_usd_cap=claimed_row.WalletAttributes.wallet_usd_cap,
        whitelist_activity=claimed_row.WalletAttributes.whitelist_activity,
    )


common_claimed_query = (
    sa.select(Claimed, WalletAttributes)
    .select_from(Claimed)
    .join(
        WalletAttributes,
        Claimed.wallet_b == WalletAttributes.wallet_b,
        isouter=False,
    )
)

common_total_count_query = (
    sa.select(sa.func.count(Claimed.wallet_b))
    .select_from(Claimed)
    .join(
        WalletAttributes,
        Claimed.wallet_b == WalletAttributes.wallet_b,
        isouter=False,
    )
)


def expected_overlap_subquery(prefix: str, contract: str) -> sa.Select:
    return sa.select(address_to_bytea(NftHolders.wallet)).where(
        sa.and_(
            NftHolders.contract_prefix == prefix, NftHolders.token_contract == contract
        )
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'request_, expected_claimed_sql',
    [
        (
            GetClaimedRequest(
                claimed_contract='0xC',
                blockchain=BlockchainType.POLYGON,
                order_by_fields=['superrank', 'wallet_usd_cap'],
                order_by_direction='DESC',
                where_field='labels',
                where_operator='contains',
                where_values=['aaa', 'bbb', 'ccc'],
                search='0xDEAD',
                limit=9,
                offset=10,
            ),
            str(
                common_claimed_query.where(
                    Claimed.claimed_contract == '0xC',
                    Claimed.blockchain == BlockchainType.POLYGON,
                    WalletAttributes.labels.contains(['aaa', 'bbb', 'ccc']),
                    sa.or_(
                        sa.func.lower(Claimed.wallet).contains('0xDEAD'.lower()),
                        sa.func.lower(WalletAttributes.ens_name).contains(
                            '0xDEAD'.lower()
                        ),
                        # temporarily disabled because of performance issues
                        # sa.func.lower(WalletAttributes.twitter_username).contains(
                        #     '0xDEAD'.lower()
                        # ),
                    ),
                )
                .order_by(
                    sa.desc(WalletAttributes.superrank).nulls_last(),
                    sa.desc(WalletAttributes.wallet_usd_cap).nulls_last(),
                    Claimed.wallet_b.asc(),
                )
                .limit(9 + 1)
                .offset(10)
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetClaimedRequest(
                claimed_contract='0xC',
                where_field='tx_count',
                where_operator='eq',
                where_values=['10'],
            ),
            str(
                common_claimed_query.where(
                    Claimed.claimed_contract == '0xC',
                    WalletAttributes.tx_count == 10,
                )
                .order_by(Claimed.wallet_b.asc())
                .limit(MAX_LIMIT + 1)
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetClaimedRequest(
                claimed_contract='0xC',
                where_field='ens_name',
                where_operator='ne',
                where_values=['black.eth'],
            ),
            str(
                common_claimed_query.where(
                    Claimed.claimed_contract == '0xC',
                    WalletAttributes.ens_name != 'black.eth',
                )
                .order_by(Claimed.wallet_b.asc())
                .limit(MAX_LIMIT + 1)
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetClaimedRequest(
                claimed_contract='bar',
                overlap_audiences=[
                    '0x0000000000000000000000000000000000000000',
                    '-0x1000000000000000000000000000000000000000',
                    '0xDEAD',  # wrong address should be ignored
                ],
            ),
            str(
                common_claimed_query.where(
                    Claimed.wallet_b.in_(
                        expected_overlap_subquery(
                            '0x0', '0x0000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(
                    Claimed.wallet_b.notin_(
                        expected_overlap_subquery(
                            '0x1', '0x1000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(Claimed.claimed_contract == 'bar')
                .order_by(sa.asc(Claimed.wallet_b))
                .limit(MAX_LIMIT + 1)
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
    ],
)
async def test_fetch_claimed(repository, claimed_row, request_, expected_claimed_sql):
    repository.session.s.execute.return_value = [claimed_row]

    await repository.fetch_claimed(request_)

    # Check that the claimed query is built correctly
    assert repository.session.s.execute.call_count == 1
    claimed_actual_sql = str(
        repository.session.s.execute.call_args[0][0].compile(
            compile_kwargs={"literal_binds": True}
        )
    )
    assert claimed_actual_sql == expected_claimed_sql


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
            GetClaimedAggregationResponse(values=[42]),
        ),
        (
            MagicMock(
                mappings=MagicMock(
                    return_value=MagicMock(
                        first=MagicMock(return_value={"c3": 42, "c1": 10, "c2": 500})
                    )
                )
            ),
            GetClaimedAggregationResponse(values=[42, 10, 500]),
        ),
    ],
)
async def test_claimed_aggregate_mapping(repository, query_result, expected_result):
    repository.session.s.execute.return_value = query_result

    result = await repository.fetch_claimed_aggregation(
        GetClaimedAggregationRequest(
            claimed_contract="0xC", agg_type="count", agg_field="wallet"
        )
    )

    assert result == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'request_, expected_sql',
    [
        (
            GetClaimedRequest(
                claimed_contract='foo',
                limit=10,
                offset=10,
            ),
            str(
                common_total_count_query.where(
                    Claimed.claimed_contract == 'foo'
                ).compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetClaimedRequest(
                claimed_contract='0xC',
                blockchain=BlockchainType.POLYGON,
                order_by_field='superrank',
                order_by_direction='DESC',
                where_field='labels',
                where_operator='contains',
                where_values=['aaa', 'bbb', 'ccc'],
                search='0xDEAD',
                limit=9,
                offset=10,
            ),
            str(
                common_total_count_query.where(
                    Claimed.claimed_contract == '0xC',
                    Claimed.blockchain == BlockchainType.POLYGON,
                    WalletAttributes.labels.contains(['aaa', 'bbb', 'ccc']),
                    sa.or_(
                        sa.func.lower(Claimed.wallet).contains('0xDEAD'.lower()),
                        sa.func.lower(WalletAttributes.ens_name).contains(
                            '0xDEAD'.lower()
                        ),
                        # temporarily disabled because of performance issues
                        # sa.func.lower(WalletAttributes.twitter_username).contains(
                        #     '0xDEAD'.lower()
                        # ),
                    ),
                ).compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetClaimedRequest(
                claimed_contract='bar',
                overlap_audiences=[
                    '0x0000000000000000000000000000000000000000',
                    '-0x1000000000000000000000000000000000000000',
                    '0xDEAD',  # wrong address should be ignored
                ],
            ),
            str(
                common_total_count_query.where(
                    Claimed.wallet_b.in_(
                        expected_overlap_subquery(
                            '0x0', '0x0000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(
                    Claimed.wallet_b.notin_(
                        expected_overlap_subquery(
                            '0x1', '0x1000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(Claimed.claimed_contract == 'bar')
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
    ],
)
async def test_fetch_claimed_count(repository, request_, expected_sql):
    repository.session.s.scalar.return_value = 44
    res = await repository.fetch_claimed_count(request_)

    assert repository.session.s.scalar.call_count == 1
    total_count_actual_sql = str(
        repository.session.s.scalar.call_args[0][0].compile(
            compile_kwargs={"literal_binds": True}
        )
    )

    assert total_count_actual_sql == expected_sql
    assert res == 44


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_, expected_sql",
    [
        # simple agg functions
        (
            GetClaimedAggregationRequest(
                claimed_contract="0xC",
                agg_type="count",
                agg_field="twitter_url",
                where_field="twitter_url",
                where_values=[None],
                where_operator="ne",
                search="0xDEAD",
            ),
            str(
                sa.select(sa.func.count(WalletAttributes.twitter_url))
                .select_from(
                    sa.join(
                        Claimed,
                        WalletAttributes,
                        Claimed.wallet_b == WalletAttributes.wallet_b,
                        isouter=False,
                    )
                )
                .where(
                    Claimed.claimed_contract == '0xC',
                    WalletAttributes.twitter_url != None,
                )
                .where(
                    sa.or_(
                        sa.func.lower(Claimed.wallet).contains('0xdead'),
                        sa.func.lower(WalletAttributes.ens_name).contains('0xdead'),
                        # temporarily disabled because of performance issues
                        # sa.func.lower(WalletAttributes.twitter_username).contains(
                        #     '0xdead'
                        # ),
                    )
                )
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetClaimedAggregationRequest(
                claimed_contract="0xB",
                agg_type="sum",
                agg_field="wallet_usd_cap",
                where_field="wallet_usd_cap",
            ),
            str(
                sa.select(sa.func.sum(WalletAttributes.wallet_usd_cap))
                .select_from(
                    sa.join(
                        Claimed,
                        WalletAttributes,
                        Claimed.wallet_b == WalletAttributes.wallet_b,
                        isouter=False,
                    )
                )
                .where(
                    Claimed.claimed_contract == '0xB',
                )
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        # agg functions with bucket interval
        (
            GetClaimedAggregationRequest(
                claimed_contract="0xF",
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
                .select_from(
                    sa.join(
                        Claimed,
                        WalletAttributes,
                        Claimed.wallet_b == WalletAttributes.wallet_b,
                        isouter=False,
                    )
                )
                .where(
                    Claimed.claimed_contract == '0xF',
                )
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        # agg functions with bucket values
        (
            GetClaimedAggregationRequest(
                claimed_contract="0xF",
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
                .select_from(
                    sa.join(
                        Claimed,
                        WalletAttributes,
                        Claimed.wallet_b == WalletAttributes.wallet_b,
                        isouter=False,
                    )
                )
                .where(
                    Claimed.claimed_contract == '0xF',
                )
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        # overlapped audience
        (
            GetClaimedAggregationRequest(
                claimed_contract="bar",
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
                .select_from(
                    sa.join(
                        Claimed,
                        WalletAttributes,
                        Claimed.wallet_b == WalletAttributes.wallet_b,
                        isouter=False,
                    )
                )
                .where(
                    Claimed.claimed_contract == 'bar',
                )
                .where(
                    Claimed.wallet_b.in_(
                        expected_overlap_subquery(
                            '0x0', '0x0000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(
                    Claimed.wallet_b.notin_(
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
async def test_fetch_claimed_aggregation(repository, request_, expected_sql):
    mocked_result = MagicMock()
    mocked_result.mappings.first.return_value = {'count': 42}
    repository.session.s.execute.return_value = mocked_result

    await repository.fetch_claimed_aggregation(request_)

    # Check that the aggregation query is built correctly
    assert repository.session.s.execute.call_count == 1
    actual_sql = str(
        repository.session.s.execute.call_args[0][0].compile(
            compile_kwargs={"literal_binds": True}
        )
    )
    assert actual_sql == expected_sql
