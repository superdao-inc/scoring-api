from app.common.helpers import address_to_bytea
import pytest
import datetime
from unittest.mock import AsyncMock, MagicMock
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.common.schemas import MAX_LIMIT
from app.fixed_list.models import FixedListItem as FixedListItemModel
from app.nft_holders.models import NftHolders
from app.fixed_list.repository import FixedListRepository
from app.fixed_list.schemas import (
    FixedListItem,
    GetFixedListAggregationRequest,
    GetFixedListRequest,
)

from app.wallet.models import WalletAttributes


def coalesce(field: sa.Column) -> sa.Column:
    return sa.func.coalesce(field, 0).label(field.name)


@pytest.fixture()
def session():
    class AsyncMockSessionMaker:
        s = AsyncMock(add_all=MagicMock())

        async def __aenter__(self, *args, **kwargs):
            return self.s

        async def __aexit__(self, *args, **kwargs):
            pass

    return AsyncMockSessionMaker


@pytest.fixture()
def repository(session):
    return FixedListRepository(session)


@pytest.fixture()
def fixed_list_row():
    mocked_row = MagicMock()
    mocked_row.FixedListItem = FixedListItemModel(list_id='test_list', wallet='0x1')
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
async def test_fixed_list_mapping(repository, fixed_list_row):
    repository.session.s.execute.return_value = [fixed_list_row]

    request = GetFixedListRequest(list_id='test_list')
    items, has_more = await repository.get_list(request)

    assert len(items) == 1
    assert not has_more
    assert items[0] == FixedListItem(
        list_id=fixed_list_row.FixedListItem.list_id,
        wallet=fixed_list_row.FixedListItem.wallet,
        superrank=fixed_list_row.WalletAttributes.superrank,
        created_at=fixed_list_row.WalletAttributes.created_at.timestamp(),
        ens_name=fixed_list_row.WalletAttributes.ens_name,
        labels=fixed_list_row.WalletAttributes.labels,
        nfts_count=fixed_list_row.WalletAttributes.nfts_count,
        twitter_avatar_url=fixed_list_row.WalletAttributes.twitter_avatar_url,
        twitter_followers_count=fixed_list_row.WalletAttributes.twitter_followers_count,
        twitter_url=fixed_list_row.WalletAttributes.twitter_url,
        twitter_username=fixed_list_row.WalletAttributes.twitter_username,
        tx_count=fixed_list_row.WalletAttributes.tx_count,
        last_month_tx_count=fixed_list_row.WalletAttributes.last_month_tx_count,
        last_month_in_volume=fixed_list_row.WalletAttributes.last_month_in_volume,
        last_month_out_volume=fixed_list_row.WalletAttributes.last_month_out_volume,
        last_month_volume=fixed_list_row.WalletAttributes.last_month_volume,
        wallet_usd_cap=fixed_list_row.WalletAttributes.wallet_usd_cap,
        whitelist_activity=fixed_list_row.WalletAttributes.whitelist_activity,
    )


common_list_query = (
    sa.select(FixedListItemModel, WalletAttributes)
    .select_from(FixedListItemModel)
    .join(
        WalletAttributes,
        FixedListItemModel.wallet_b == WalletAttributes.wallet_b,
        isouter=False,
    )
)

common_total_count_query = (
    sa.select(sa.func.count(FixedListItemModel.wallet_b))
    .select_from(FixedListItemModel)
    .join(
        WalletAttributes,
        FixedListItemModel.wallet_b == WalletAttributes.wallet_b,
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
    'request_, expected_sql',
    [
        (
            GetFixedListRequest(
                list_id='test_list',
                limit=10,
                offset=10,
            ),
            str(
                common_total_count_query.where(
                    FixedListItemModel.list_id == 'test_list'
                ).compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetFixedListRequest(
                list_id='test_list',
                order_by_fields=['wallet_usd_cap'],
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
                    FixedListItemModel.list_id == 'test_list',
                    WalletAttributes.labels.contains(['aaa', 'bbb', 'ccc']),
                    sa.or_(
                        sa.func.lower(FixedListItemModel.wallet).contains(
                            '0xDEAD'.lower()
                        ),
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
            GetFixedListRequest(
                list_id='bar',
                overlap_audiences=[
                    '0x0000000000000000000000000000000000000000',
                    '-0x1000000000000000000000000000000000000000',
                    '0xDEAD',  # wrong address should be ignored
                ],
            ),
            str(
                common_total_count_query.where(
                    FixedListItemModel.wallet_b.in_(
                        expected_overlap_subquery(
                            '0x0', '0x0000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(
                    FixedListItemModel.wallet_b.notin_(
                        expected_overlap_subquery(
                            '0x1', '0x1000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(FixedListItemModel.list_id == 'bar')
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
    ],
)
async def test_fetch_list_count(repository, request_, expected_sql):
    repository.session.s.scalar.return_value = 42

    res = await repository.get_list_count(request_)

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
    'request_, expected_sql',
    [
        (
            GetFixedListRequest(
                list_id='test_list',
                order_by_field='wallet_usd_cap',
                order_by_direction='DESC',
                where_field='labels',
                where_operator='contains',
                where_values=['aaa', 'bbb', 'ccc'],
                search='0xDEAD',
                limit=9,
                offset=1,
            ),
            str(
                common_list_query.where(
                    FixedListItemModel.list_id == 'test_list',
                    WalletAttributes.labels.contains(['aaa', 'bbb', 'ccc']),
                    sa.or_(
                        sa.func.lower(FixedListItemModel.wallet).contains(
                            '0xDEAD'.lower()
                        ),
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
                    sa.desc(WalletAttributes.wallet_usd_cap).nulls_last(),
                    FixedListItemModel.wallet_b.asc(),
                )
                .limit(9 + 1)
                .offset(1)
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetFixedListRequest(
                list_id='test_list',
                where_field='tx_count',
                where_operator='eq',
                where_values=['10'],
            ),
            str(
                common_list_query.where(
                    FixedListItemModel.list_id == 'test_list',
                    WalletAttributes.tx_count == 10,
                )
                .order_by(FixedListItemModel.wallet_b.asc())
                .limit(MAX_LIMIT + 1)
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetFixedListRequest(
                list_id='test_list',
                where_field='ens_name',
                where_operator='ne',
                where_values=['black.eth'],
            ),
            str(
                common_list_query.where(
                    FixedListItemModel.list_id == 'test_list',
                    WalletAttributes.ens_name != 'black.eth',
                )
                .order_by(FixedListItemModel.wallet_b.asc())
                .limit(MAX_LIMIT + 1)
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetFixedListRequest(
                list_id='bar',
                overlap_audiences=[
                    '0x0000000000000000000000000000000000000000',
                    '-0x1000000000000000000000000000000000000000',
                    '0xDEAD',  # wrong address should be ignored
                ],
            ),
            str(
                common_list_query.where(
                    FixedListItemModel.wallet_b.in_(
                        expected_overlap_subquery(
                            '0x0', '0x0000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(
                    FixedListItemModel.wallet_b.notin_(
                        expected_overlap_subquery(
                            '0x1', '0x1000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(FixedListItemModel.list_id == 'bar')
                .order_by(sa.asc(FixedListItemModel.wallet_b))
                .limit(MAX_LIMIT + 1)
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
    ],
)
async def test_fetch_list(repository, fixed_list_row, request_, expected_sql):
    repository.session.s.execute.return_value = [fixed_list_row]

    await repository.get_list(request_)

    # Check that the audience query is built correctly
    assert repository.session.s.execute.call_count == 1
    audience_actual_sql = str(
        repository.session.s.execute.call_args[0][0].compile(
            compile_kwargs={"literal_binds": True}
        )
    )
    assert audience_actual_sql == expected_sql


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
            [42],
        ),
        (
            MagicMock(
                mappings=MagicMock(
                    return_value=MagicMock(
                        first=MagicMock(return_value={"c3": 42, "c1": 10, "c2": 500})
                    )
                )
            ),
            [42, 10, 500],
        ),
    ],
)
async def test_list_aggregate_mapping(repository, query_result, expected_result):
    repository.session.s.execute.return_value = query_result

    result = await repository.fetch_list_aggregation(
        GetFixedListAggregationRequest(
            list_id="test_list", agg_type="count", agg_field="wallet"
        )
    )

    assert result == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_, expected_sql",
    [
        # simple agg functions
        (
            GetFixedListAggregationRequest(
                list_id="test_list",
                agg_type="count",
                agg_field="twitter_url",
                where_field="twitter_url",
                where_values=[None],
                where_operator="ne",
            ),
            str(
                sa.select(sa.func.count(WalletAttributes.twitter_url))
                .select_from(
                    sa.join(
                        FixedListItemModel,
                        WalletAttributes,
                        FixedListItemModel.wallet_b == WalletAttributes.wallet_b,
                        isouter=False,
                    )
                )
                .where(
                    FixedListItemModel.list_id == 'test_list',
                    WalletAttributes.twitter_url != None,
                )
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetFixedListAggregationRequest(
                list_id="test_list",
                agg_type="sum",
                agg_field="wallet_usd_cap",
                where_field="wallet_usd_cap",
            ),
            str(
                sa.select(sa.func.sum(WalletAttributes.wallet_usd_cap))
                .select_from(
                    sa.join(
                        FixedListItemModel,
                        WalletAttributes,
                        FixedListItemModel.wallet_b == WalletAttributes.wallet_b,
                        isouter=False,
                    )
                )
                .where(
                    FixedListItemModel.list_id == 'test_list',
                )
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        # agg functions with bucket interval
        (
            GetFixedListAggregationRequest(
                list_id="test_list",
                agg_type="count_bucket_intervals",
                agg_field="wallet_usd_cap",
                buckets=["t:99", "f:100;t:999", "f:1000"],
            ),
            str(
                sa.select(
                    sa.func.count(coalesce(WalletAttributes.wallet_usd_cap))
                    .filter(coalesce(WalletAttributes.wallet_usd_cap) <= 99),
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
                        FixedListItemModel,
                        WalletAttributes,
                        FixedListItemModel.wallet_b == WalletAttributes.wallet_b,
                        isouter=False,
                    )
                )
                .where(
                    FixedListItemModel.list_id == 'test_list',
                )
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        # agg functions with bucket values
        (
            GetFixedListAggregationRequest(
                list_id="test_list",
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
                        FixedListItemModel,
                        WalletAttributes,
                        FixedListItemModel.wallet_b == WalletAttributes.wallet_b,
                        isouter=False,
                    )
                )
                .where(
                    FixedListItemModel.list_id == 'test_list',
                )
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        # overlapped audience
        (
            GetFixedListAggregationRequest(
                list_id="bar",
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
                        FixedListItemModel,
                        WalletAttributes,
                        FixedListItemModel.wallet_b == WalletAttributes.wallet_b,
                        isouter=False,
                    )
                )
                .where(
                    FixedListItemModel.list_id == 'bar',
                )
                .where(
                    FixedListItemModel.wallet_b.in_(
                        expected_overlap_subquery(
                            '0x0', '0x0000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(
                    FixedListItemModel.wallet_b.notin_(
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
async def test_fetch_list_aggregation(repository, request_, expected_sql):
    mocked_result = MagicMock()
    mocked_result.mappings.first.return_value = {'count': 42}
    repository.session.s.execute.return_value = mocked_result

    await repository.fetch_list_aggregation(request_)

    # Check that the aggregation query is built correctly
    assert repository.session.s.execute.call_count == 1
    actual_sql = str(
        repository.session.s.execute.call_args[0][0].compile(
            compile_kwargs={"literal_binds": True}
        )
    )
    assert actual_sql == expected_sql


@pytest.mark.asyncio
async def test_save_fixed_list_items(repository: FixedListRepository):
    # arrange
    models = [
        FixedListItemModel(list_id='test_list', wallet='0x11'),
        FixedListItemModel(list_id='test_list', wallet='0x22'),
    ]
    repository.session.s.add_all.return_value = None
    repository.session.s.commit.return_value = None

    expected_inserted_values = [
        {
            "list_id": model.list_id,
            "wallet": model.wallet,
            "wallet_b": sa.func.decode(sa.func.substring(model.wallet, 3), 'hex')
        }
        for model in models
    ]

    expected_sql = str(
        pg_insert(FixedListItemModel)
        .values(expected_inserted_values)
        .on_conflict_do_nothing()
        .compile(compile_kwargs={"literal_binds": True})
    )

    # act
    await repository.save_fixed_list_items(models)

    # assert
    repository.session.s.execute.assert_called_once()
    actual_sql = str(
        repository.session.s.execute.call_args[0][0].compile(
            compile_kwargs={"literal_binds": True}
        )
    )
    assert actual_sql == expected_sql
    repository.session.s.commit.assert_called_once()
