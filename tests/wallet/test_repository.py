import pytest
import datetime
from unittest.mock import AsyncMock, MagicMock
import sqlalchemy as sa

from app.wallet.models import WalletAttributes
from app.wallet.repository import WalletRepository
from app.wallet.schemas import (
    GetWalletAttributesRequest,
    GetWalletsLeaderboardRequest,
    GetSimilarWalletsAttributesRequest,
    WalletAttributesItem,
)


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
    return WalletRepository(session)


@pytest.fixture()
def attributes_row():
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
        twitter_location='location',
        twitter_bio='bio',
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
async def test_wallet_attributes_mapping(repository, attributes_row):
    repository.session.s.execute.return_value = MagicMock(
        one_or_none=MagicMock(return_value=attributes_row)
    )

    request = GetWalletAttributesRequest(wallet='0x1')
    item = await repository.fetch_attributes(request)

    assert item == WalletAttributesItem(
        wallet=request.wallet,
        superrank=attributes_row.WalletAttributes.superrank,
        created_at=attributes_row.WalletAttributes.created_at.timestamp(),
        ens_name=attributes_row.WalletAttributes.ens_name,
        labels=attributes_row.WalletAttributes.labels,
        nfts_count=attributes_row.WalletAttributes.nfts_count,
        twitter_avatar_url=attributes_row.WalletAttributes.twitter_avatar_url,
        twitter_followers_count=attributes_row.WalletAttributes.twitter_followers_count,
        twitter_url=attributes_row.WalletAttributes.twitter_url,
        twitter_username=attributes_row.WalletAttributes.twitter_username,
        twitter_location=attributes_row.WalletAttributes.twitter_location,
        twitter_bio=attributes_row.WalletAttributes.twitter_bio,
        tx_count=attributes_row.WalletAttributes.tx_count,
        last_month_tx_count=attributes_row.WalletAttributes.last_month_tx_count,
        last_month_in_volume=attributes_row.WalletAttributes.last_month_in_volume,
        last_month_out_volume=attributes_row.WalletAttributes.last_month_out_volume,
        last_month_volume=attributes_row.WalletAttributes.last_month_volume,
        wallet_usd_cap=attributes_row.WalletAttributes.wallet_usd_cap,
        whitelist_activity=attributes_row.WalletAttributes.whitelist_activity,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'request_, expected_sql',
    [
        (
            GetWalletAttributesRequest(wallet='0x11'),
            str(
                sa.select(WalletAttributes)
                .where(WalletAttributes.wallet_b == sa.func.decode('11', 'hex'))
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetWalletAttributesRequest(wallet='0x1234'),
            str(
                sa.select(WalletAttributes)
                .where(WalletAttributes.wallet_b == sa.func.decode('1234', 'hex'))
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
    ],
)
async def test_fetch_attributes(repository, attributes_row, request_, expected_sql):
    repository.session.s.execute.return_value = MagicMock(
        one_or_none=MagicMock(return_value=attributes_row)
    )

    await repository.fetch_attributes(request_)

    # Check that the query is built correctly
    assert repository.session.s.execute.call_count == 1
    actual_sql = str(
        repository.session.s.execute.call_args[0][0].compile(
            compile_kwargs={"literal_binds": True}
        )
    )
    assert actual_sql == expected_sql


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'request_, expected_sql',
    [
        (
            GetWalletsLeaderboardRequest(
                order_by_field='superrank', order_by_direction='ASC', limit=25
            ),
            str(
                sa.select(WalletAttributes)
                .order_by(
                    WalletAttributes.superrank.asc().nulls_last(),
                    WalletAttributes.wallet_b.asc(),
                )
                .limit(25)
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetWalletsLeaderboardRequest(
                order_by_fields=['wallet_usd_cap', 'superrank'],
                order_by_direction='DESC',
                limit=50,
            ),
            str(
                sa.select(WalletAttributes)
                .order_by(
                    WalletAttributes.wallet_usd_cap.desc().nulls_last(),
                    WalletAttributes.superrank.desc().nulls_last(),
                    WalletAttributes.wallet_b.asc(),
                )
                .limit(50)
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
    ],
)
async def test_fetch_leaderboard(repository, attributes_row, request_, expected_sql):
    repository.session.s.execute.return_value = MagicMock(
        one_or_none=MagicMock(return_value=attributes_row)
    )

    await repository.fetch_leaderboard(request_)

    # Check that the query is built correctly
    assert repository.session.s.execute.call_count == 1
    actual_sql = str(
        repository.session.s.execute.call_args[0][0].compile(
            compile_kwargs={"literal_binds": True}
        )
    )
    assert actual_sql == expected_sql


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'request_, expected_sql',
    [
        (
            GetSimilarWalletsAttributesRequest(similar_wallets=['0x42'], limit=25),
            str(
                sa.select(WalletAttributes)
                .where(WalletAttributes.wallet.in_(['0x42']))
                .order_by(
                    WalletAttributes.superrank.desc().nulls_last(),
                    WalletAttributes.wallet_b.asc(),
                )
                .limit(25)
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
    ],
)
async def test_fetch_wallets_attributes(
    repository, attributes_row, request_, expected_sql
):
    repository.session.s.execute.return_value = MagicMock(
        one_or_none=MagicMock(return_value=attributes_row)
    )

    await repository.fetch_wallets_attributes(request_)

    # Check that the query is built correctly
    assert repository.session.s.execute.call_count == 1
    actual_sql = str(
        repository.session.s.execute.call_args[0][0].compile(
            compile_kwargs={"literal_binds": True}
        )
    )
    assert actual_sql == expected_sql
