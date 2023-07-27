from app.common.helpers import address_to_bytea
import pytest
import datetime
from time import time
from unittest.mock import AsyncMock, MagicMock
import sqlalchemy as sa
from app.common.schemas import MAX_LIMIT

from app.wallet.models import WalletAttributes
from app.analytics.models import (
    WalletLastEvents,
    WalletEventsType,
    AnalyticsEventsSources,
)
from app.nft_holders.models import NftHolders
from app.analytics.repository import AnalyticsRepository
from app.analytics.schemas import (
    AnalyticsItem,
    GetAggregationsRequest,
    GetAnalyticsRequest,
    GetEventsStatsRequest,
)
from app.analytics.service import DEFAULT_TOP_SOURCES_COUNT


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
    return AnalyticsRepository(session)


@pytest.fixture()
def analytics_row():
    now = time()
    mocked_row = MagicMock()
    mocked_row.WalletLastEvents = WalletLastEvents(
        address='0x1',
        tracker_id='foo',
        last_event=WalletEventsType('FORM_SUBMIT'),
        last_event_timestamp=datetime.datetime.fromtimestamp(now),
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
async def test_analytics_mapping(repository, analytics_row):
    repository.session.s.execute.return_value = [analytics_row]
    repository.session.s.scalar.return_value = 1

    request = GetAnalyticsRequest(tracker_id='foo')
    items, total = await repository.fetch_analytics(request)

    assert len(items) == 1
    assert total == 1
    assert items[0] == AnalyticsItem(
        tracker_id=analytics_row.WalletLastEvents.tracker_id,
        wallet=analytics_row.WalletLastEvents.address,
        last_event=analytics_row.WalletLastEvents.last_event.value,
        last_event_timestamp=int(
            analytics_row.WalletLastEvents.last_event_timestamp.timestamp()
        ),
        superrank=analytics_row.WalletAttributes.superrank,
        created_at=analytics_row.WalletAttributes.created_at.timestamp(),
        ens_name=analytics_row.WalletAttributes.ens_name,
        labels=analytics_row.WalletAttributes.labels,
        nfts_count=analytics_row.WalletAttributes.nfts_count,
        twitter_avatar_url=analytics_row.WalletAttributes.twitter_avatar_url,
        twitter_followers_count=analytics_row.WalletAttributes.twitter_followers_count,
        twitter_url=analytics_row.WalletAttributes.twitter_url,
        twitter_username=analytics_row.WalletAttributes.twitter_username,
        tx_count=analytics_row.WalletAttributes.tx_count,
        last_month_tx_count=analytics_row.WalletAttributes.last_month_tx_count,
        last_month_in_volume=analytics_row.WalletAttributes.last_month_in_volume,
        last_month_out_volume=analytics_row.WalletAttributes.last_month_out_volume,
        last_month_volume=analytics_row.WalletAttributes.last_month_volume,
        wallet_usd_cap=analytics_row.WalletAttributes.wallet_usd_cap,
        whitelist_activity=analytics_row.WalletAttributes.whitelist_activity,
    )


common_analytics_query = (
    sa.select(WalletLastEvents, WalletAttributes)
    .select_from(WalletLastEvents)
    .join(
        WalletAttributes,
        WalletLastEvents.address == WalletAttributes.wallet,
        isouter=False,
    )
)

common_total_count_query = (
    sa.select(sa.func.count(WalletLastEvents.address))
    .select_from(WalletLastEvents)
    .join(
        WalletAttributes,
        WalletLastEvents.address == WalletAttributes.wallet,
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
    'request_, expected_analytics_sql, expected_total_count_sql',
    [
        (
            GetAnalyticsRequest(
                tracker_id='foo',
                order_by_field='nfts_count',
                order_by_direction='ASC',
                where_field='labels',
                where_operator='contains',
                where_values=['aaa', 'bbb', 'ccc'],
                search='0xDEAD',
                limit=9,
                offset=1,
            ),
            str(
                common_analytics_query.where(
                    WalletLastEvents.tracker_id == 'foo',
                    WalletAttributes.labels.contains(['aaa', 'bbb', 'ccc']),
                    sa.or_(
                        sa.func.lower(WalletLastEvents.address).contains(
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
                    sa.asc(WalletAttributes.nfts_count).nulls_last(),
                    sa.asc(WalletLastEvents.address),
                )
                .limit(9 + 1)
                .offset(1)
                .compile(compile_kwargs={"literal_binds": True})
            ),
            str(
                common_total_count_query.where(
                    WalletLastEvents.tracker_id == 'foo',
                    WalletAttributes.labels.contains(['aaa', 'bbb', 'ccc']),
                    sa.or_(
                        sa.func.lower(WalletLastEvents.address).contains(
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
            GetAnalyticsRequest(
                tracker_id='bar',
                where_field='nfts_count',
                where_operator='eq',
                where_values=['10'],
            ),
            str(
                common_analytics_query.where(
                    WalletLastEvents.tracker_id == 'bar',
                    WalletAttributes.nfts_count == 10,
                )
                .order_by(sa.asc(WalletLastEvents.address))
                .limit(MAX_LIMIT + 1)
                .compile(compile_kwargs={"literal_binds": True})
            ),
            str(
                common_total_count_query.where(
                    WalletLastEvents.tracker_id == 'bar',
                    WalletAttributes.nfts_count == 10,
                ).compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetAnalyticsRequest(
                tracker_id='bar',
                where_field='ens_name',
                where_operator='ne',
                where_values=['black.eth'],
            ),
            str(
                common_analytics_query.where(
                    WalletLastEvents.tracker_id == 'bar',
                    WalletAttributes.ens_name != 'black.eth',
                )
                .order_by(sa.asc(WalletLastEvents.address))
                .limit(MAX_LIMIT + 1)
                .compile(compile_kwargs={"literal_binds": True})
            ),
            str(
                common_total_count_query.where(
                    WalletLastEvents.tracker_id == 'bar',
                    WalletAttributes.ens_name != 'black.eth',
                ).compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetAnalyticsRequest(
                tracker_id='bar',
                overlap_audiences=[
                    '0x0000000000000000000000000000000000000000',
                    '-0x1000000000000000000000000000000000000000',
                    '0xDEAD',  # wrong address should be ignored
                ],
            ),
            str(
                common_analytics_query.where(
                    WalletLastEvents.address.in_(
                        expected_overlap_subquery(
                            '0x0', '0x0000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(
                    WalletLastEvents.address.notin_(
                        expected_overlap_subquery(
                            '0x1', '0x1000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(WalletLastEvents.tracker_id == 'bar')
                .order_by(sa.asc(WalletLastEvents.address))
                .limit(MAX_LIMIT + 1)
                .compile(compile_kwargs={"literal_binds": True})
            ),
            str(
                common_total_count_query.where(
                    WalletLastEvents.address.in_(
                        expected_overlap_subquery(
                            '0x0', '0x0000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(
                    WalletLastEvents.address.notin_(
                        expected_overlap_subquery(
                            '0x1', '0x1000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(WalletLastEvents.tracker_id == 'bar')
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
    ],
)
async def test_fetch_analytics(
    repository,
    analytics_row,
    request_,
    expected_analytics_sql,
    expected_total_count_sql,
):
    repository.session.s.execute.return_value = [analytics_row]

    await repository.fetch_analytics(request_)

    # Check that the total_count query is built correctly
    assert repository.session.s.scalar.call_count == 1
    total_count_actual_sql = str(
        repository.session.s.scalar.call_args[0][0].compile(
            compile_kwargs={"literal_binds": True}
        )
    )

    assert total_count_actual_sql == expected_total_count_sql

    # Check that the analytics query is built correctly
    assert repository.session.s.execute.call_count == 1
    analytics_actual_sql = str(
        repository.session.s.execute.call_args[0][0].compile(
            compile_kwargs={"literal_binds": True}
        )
    )
    assert analytics_actual_sql == expected_analytics_sql


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
async def test_analytics_aggregate_mapping(repository, query_result, expected_result):
    repository.session.s.execute.return_value = query_result

    result = await repository.fetch_analytics_aggregation(
        GetAggregationsRequest(tracker_id="foo", agg_type="count", agg_field="address")
    )

    assert result == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_, expected_sql",
    [
        # simple agg functions
        (
            GetAggregationsRequest(
                tracker_id="foo",
                agg_type="count",
                agg_field="twitter_url",
                where_field="twitter_url",
                where_values=[None],
                where_operator="ne",
                search='0xDEAD',
            ),
            str(
                sa.select(sa.func.count(WalletAttributes.twitter_url))
                .select_from(
                    sa.join(
                        WalletLastEvents,
                        WalletAttributes,
                        WalletLastEvents.address == WalletAttributes.wallet,
                        isouter=False,
                    )
                )
                .where(
                    WalletLastEvents.tracker_id == 'foo',
                    WalletAttributes.twitter_url != None,
                )
                .where(
                    sa.or_(
                        sa.func.lower(WalletLastEvents.address).contains(
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
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetAggregationsRequest(
                tracker_id="bar",
                agg_type="sum",
                agg_field="wallet_usd_cap",
                where_field="wallet_usd_cap",
            ),
            str(
                sa.select(sa.func.sum(WalletAttributes.wallet_usd_cap))
                .select_from(
                    sa.join(
                        WalletLastEvents,
                        WalletAttributes,
                        WalletLastEvents.address == WalletAttributes.wallet,
                        isouter=False,
                    )
                )
                .where(
                    WalletLastEvents.tracker_id == 'bar',
                )
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        # agg functions with bucket interval
        (
            GetAggregationsRequest(
                tracker_id="foo",
                agg_type="count_bucket_intervals",
                agg_field="wallet_usd_cap",
                buckets=["t:99", "f:100;t:999", "f:1000"],
            ),
            str(
                sa.select(
                    sa.func.count(coalesce(WalletAttributes.wallet_usd_cap))
                    .filter(
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
                        WalletLastEvents,
                        WalletAttributes,
                        WalletLastEvents.address == WalletAttributes.wallet,
                        isouter=False,
                    )
                )
                .where(
                    WalletLastEvents.tracker_id == 'foo',
                )
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        # agg functions with bucket values
        (
            GetAggregationsRequest(
                tracker_id="foo",
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
                        WalletLastEvents,
                        WalletAttributes,
                        WalletLastEvents.address == WalletAttributes.wallet,
                        isouter=False,
                    )
                )
                .where(
                    WalletLastEvents.tracker_id == 'foo',
                )
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetAggregationsRequest(
                tracker_id="bar",
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
                        WalletLastEvents,
                        WalletAttributes,
                        WalletLastEvents.address == WalletAttributes.wallet,
                        isouter=False,
                    )
                )
                .where(
                    WalletLastEvents.tracker_id == 'bar',
                )
                .where(
                    WalletLastEvents.address.in_(
                        expected_overlap_subquery(
                            '0x0', '0x0000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(
                    WalletLastEvents.address.notin_(
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
async def test_fetch_analytics_aggregation(repository, request_, expected_sql):
    mocked_result = MagicMock()
    mocked_result.mappings.first.return_value = {'count': 42}
    repository.session.s.execute.return_value = mocked_result

    await repository.fetch_analytics_aggregation(request_)

    # Check that the aggregation query is built correctly
    assert repository.session.s.execute.call_count == 1
    actual_sql = str(
        repository.session.s.execute.call_args[0][0].compile(
            compile_kwargs={"literal_binds": True}
        )
    )
    assert actual_sql == expected_sql


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_, expected_sql",
    [
        (
            GetEventsStatsRequest(
                tracker_id="foo", events=['bar', 'baz'], top_sources_count=3
            ),
            str(
                sa.select(
                    AnalyticsEventsSources.tracker_id,
                    AnalyticsEventsSources.event_type,
                    AnalyticsEventsSources.source,
                    AnalyticsEventsSources.count,
                )
                .where(AnalyticsEventsSources.tracker_id == 'foo')
                .where(
                    AnalyticsEventsSources.event_type.in_(['bar', 'baz']),
                )
                .where(
                    AnalyticsEventsSources.source.in_(
                        sa.select(AnalyticsEventsSources.source)
                        .where(AnalyticsEventsSources.tracker_id == 'foo')
                        .where(AnalyticsEventsSources.source != '')
                        .group_by(AnalyticsEventsSources.source)
                        .order_by(sa.func.sum(AnalyticsEventsSources.count).desc())
                        .limit(3)
                    )
                )
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetEventsStatsRequest(tracker_id="foo"),
            str(
                sa.select(
                    AnalyticsEventsSources.tracker_id,
                    AnalyticsEventsSources.event_type,
                    AnalyticsEventsSources.source,
                    AnalyticsEventsSources.count,
                )
                .where(AnalyticsEventsSources.tracker_id == 'foo')
                .where(
                    sa.sql.true(),
                )
                .where(
                    AnalyticsEventsSources.source.in_(
                        sa.select(AnalyticsEventsSources.source)
                        .where(AnalyticsEventsSources.tracker_id == 'foo')
                        .where(AnalyticsEventsSources.source != '')
                        .group_by(AnalyticsEventsSources.source)
                        .order_by(sa.func.sum(AnalyticsEventsSources.count).desc())
                        .limit(DEFAULT_TOP_SOURCES_COUNT)
                    )
                )
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
    ],
)
async def test_fetch_events_stats(repository, request_, expected_sql):
    mocked_result = MagicMock()
    mocked_result.mappings().all.return_value = [
        {'tracker_id': 'foo', 'event_type': 'bar', 'source': 'google', 'count': 42}
    ]
    repository.session.s.execute.return_value = mocked_result

    assert await repository.fetch_events_stats_sources(
        request_.tracker_id,
        request_.top_sources_count
        if request_.top_sources_count
        else DEFAULT_TOP_SOURCES_COUNT,
        request_.events if request_.events else [],
    )

    assert repository.session.s.execute.call_count == 1

    actual_sql = str(
        repository.session.s.execute.call_args[0][0].compile(
            compile_kwargs={"literal_binds": True}
        )
    )

    assert actual_sql == expected_sql
