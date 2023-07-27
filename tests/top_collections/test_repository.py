import re
import pytest
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
import sqlalchemy as sa
from app.common.enums import AudienceType, BlockchainType
from app.top_collections.models import TopCollectionsModel, TopWhitelistedCollectionsModel

from app.top_collections.repository import TopCollectionsRepository
from app.top_collections.schemas import TopCollectionsQuery


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
    return TopCollectionsRepository(session)


@pytest.fixture
def top_collections():
    return [
        TopCollectionsModel(
            chain=BlockchainType.ETHEREUM,
            audience_type=AudienceType.CLAIMED,
            audience_slug='0xdeadbeef',
            token_address='0x01',
            nft_count=42,
            holders_count=43,
            total_nft_count=44,
            total_holders_count=45,
            updated=datetime(2021, 1, 1, 0, 0, 0),
        )
    ]


@pytest.fixture
def top_whitelisted_collections():
    return [
        TopWhitelistedCollectionsModel(
            chain=BlockchainType.ETHEREUM,
            audience_type=AudienceType.CLAIMED,
            audience_slug='0xdeadbeef',
            token_address='0x02',
            nft_count=42,
            holders_count=43,
            total_nft_count=44,
            total_holders_count=45,
            updated=datetime(2021, 1, 1, 0, 0, 0),
        )
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "request_query, db_result, expected_sql",
    [
        (
            TopCollectionsQuery(
                audience_id='0xdeadbeef',
                audience_type=AudienceType.CLAIMED,
                blockchain=BlockchainType.ETHEREUM,
                top_n=15
            ),
            top_collections,
            str(
                sa.select(TopCollectionsModel)
                .where(TopCollectionsModel.audience_slug == '0xdeadbeef')
                .where(TopCollectionsModel.audience_type == 'CLAIMED')
                .where(TopCollectionsModel.chain == 'ETHEREUM')
                .limit(15)
                .order_by(
                    sa.desc(TopCollectionsModel.holders_count)
                )
                .order_by(
                    sa.desc(TopCollectionsModel.token_address)
                )
                .compile(compile_kwargs={"literal_binds": True})
            )
        ),
        (
            TopCollectionsQuery(
                audience_id='0xdeadbeef',
                audience_type=AudienceType.CLAIMED,
                blockchain=BlockchainType.ETHEREUM,
                top_n=15,
                use_whitelisted_activities=True
            ),
            top_whitelisted_collections,
            str(
                sa.select(TopWhitelistedCollectionsModel)
                .where(TopWhitelistedCollectionsModel.audience_slug == '0xdeadbeef')
                .where(TopWhitelistedCollectionsModel.audience_type == 'CLAIMED')
                .where(TopWhitelistedCollectionsModel.chain == 'ETHEREUM')
                .limit(15)
                .order_by(
                    sa.desc(TopWhitelistedCollectionsModel.holders_count)
                )
                .order_by(
                    sa.desc(TopWhitelistedCollectionsModel.token_address)
                )
                .compile(compile_kwargs={"literal_binds": True})
            )
        ),
    ]
)
async def test_fetch_top_collections(repository, request_query, db_result, expected_sql):
    repository.session.s.scalars.return_value = MagicMock(
        one_or_none=MagicMock(return_value=db_result)
    )

    await repository.get_top_collections(
        audience_id=request_query.audience_id,
        audience_type=request_query.audience_type,
        blockchain=request_query.blockchain,
        top_n=request_query.top_n,
        order_by_fields=request_query.order_by_fields,
        order_by_direction=request_query.order_by_direction,
        use_whitelisted_activities=request_query.use_whitelisted_activities
    )

    # Check that the query is built correctly
    assert repository.session.s.scalars.call_count == 1
    actual_sql = str(
        repository.session.s.scalars.call_args[0][0].compile(
            compile_kwargs={"literal_binds": True}
        )
    )

    assert actual_sql == expected_sql
