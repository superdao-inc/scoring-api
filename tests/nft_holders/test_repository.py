from app.common.helpers import address_to_bytea
import pytest
import datetime
from unittest.mock import AsyncMock, MagicMock
import sqlalchemy as sa
from app.common.schemas import MAX_LIMIT

from app.wallet.models import WalletAttributes
from app.nft_holders.models import NftHolders
from app.nft_holders.repository import NftHoldersRepository
from app.nft_holders.schemas import (
    NftHoldersItem,
    GetNftHoldersRequest,
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
    return NftHoldersRepository(session)


@pytest.fixture()
def nft_holders_row():
    mocked_row = MagicMock()
    mocked_row.NftHolders = NftHolders(
        wallet='0x1',
        contract_prefix='0xC',
        token_contract='0xC',
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
async def test_claimed_mapping(repository, nft_holders_row):
    repository.session.s.execute.return_value = [nft_holders_row]

    request = GetNftHoldersRequest(collection_address='0xC')
    items, has_more = await repository.fetch_nft_holders(request)

    assert len(items) == 1
    assert not has_more
    assert items[0] == NftHoldersItem(
        wallet=nft_holders_row.NftHolders.wallet,
        superrank=nft_holders_row.WalletAttributes.superrank,
        created_at=nft_holders_row.WalletAttributes.created_at.timestamp(),
        ens_name=nft_holders_row.WalletAttributes.ens_name,
        labels=nft_holders_row.WalletAttributes.labels,
        nfts_count=nft_holders_row.WalletAttributes.nfts_count,
        twitter_avatar_url=nft_holders_row.WalletAttributes.twitter_avatar_url,
        twitter_followers_count=nft_holders_row.WalletAttributes.twitter_followers_count,
        twitter_url=nft_holders_row.WalletAttributes.twitter_url,
        twitter_username=nft_holders_row.WalletAttributes.twitter_username,
        tx_count=nft_holders_row.WalletAttributes.tx_count,
        last_month_tx_count=nft_holders_row.WalletAttributes.last_month_tx_count,
        last_month_in_volume=nft_holders_row.WalletAttributes.last_month_in_volume,
        last_month_out_volume=nft_holders_row.WalletAttributes.last_month_out_volume,
        last_month_volume=nft_holders_row.WalletAttributes.last_month_volume,
        wallet_usd_cap=nft_holders_row.WalletAttributes.wallet_usd_cap,
        whitelist_activity=nft_holders_row.WalletAttributes.whitelist_activity,
    )


common_claimed_query = (
    sa.select(NftHolders, WalletAttributes)
    .select_from(NftHolders)
    .join(
        WalletAttributes,
        NftHolders.wallet_b == WalletAttributes.wallet_b,
        isouter=False,
    )
)

common_total_count_query = (
    sa.select(sa.func.count(NftHolders.wallet_b))
    .select_from(NftHolders)
    .join(
        WalletAttributes,
        NftHolders.wallet_b == WalletAttributes.wallet_b,
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
            GetNftHoldersRequest(
                collection_address='0xC',
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
                    NftHolders.token_contract == '0xC',
                    NftHolders.contract_prefix == '0xC',
                    WalletAttributes.labels.contains(['aaa', 'bbb', 'ccc']),
                    sa.or_(
                        sa.func.lower(NftHolders.wallet).contains('0xDEAD'.lower()),
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
                    NftHolders.wallet_b.asc(),
                )
                .limit(9 + 1)
                .offset(10)
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetNftHoldersRequest(
                collection_address='0xC',
                where_field='tx_count',
                where_operator='eq',
                where_values=['10'],
            ),
            str(
                common_claimed_query.where(
                    NftHolders.token_contract == '0xC',
                    NftHolders.contract_prefix == '0xC',
                    WalletAttributes.tx_count == 10,
                )
                .order_by(NftHolders.wallet_b.asc())
                .limit(MAX_LIMIT + 1)
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetNftHoldersRequest(
                collection_address='0xC',
                where_field='ens_name',
                where_operator='ne',
                where_values=['black.eth'],
            ),
            str(
                common_claimed_query.where(
                    NftHolders.token_contract == '0xC',
                    NftHolders.contract_prefix == '0xC',
                    WalletAttributes.ens_name != 'black.eth',
                )
                .order_by(NftHolders.wallet_b.asc())
                .limit(MAX_LIMIT + 1)
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
        (
            GetNftHoldersRequest(
                collection_address='bar',
                overlap_audiences=[
                    '0x4000000000000000000000000000000000000000',
                    '-0x1000000000000000000000000000000000000000',
                    '0xDEAD',  # wrong address should be ignored
                ],
            ),
            str(
                common_claimed_query.where(
                    NftHolders.wallet_b.in_(
                        expected_overlap_subquery(
                            '0x4', '0x4000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(
                    NftHolders.wallet_b.notin_(
                        expected_overlap_subquery(
                            '0x1', '0x1000000000000000000000000000000000000000'
                        )
                    )
                )
                .where(
                    NftHolders.token_contract == 'bar',
                    NftHolders.contract_prefix == 'bar',
                )
                .order_by(sa.asc(NftHolders.wallet_b))
                .limit(MAX_LIMIT + 1)
                .compile(compile_kwargs={"literal_binds": True})
            ),
        ),
    ],
)
async def test_fetch_claimed(
    repository, nft_holders_row, request_, expected_claimed_sql
):
    repository.session.s.execute.return_value = [nft_holders_row]

    await repository.fetch_nft_holders(request_)

    # Check that the nft_holders query is built correctly
    assert repository.session.s.execute.call_count == 1
    claimed_actual_sql = str(
        repository.session.s.execute.call_args[0][0].compile(
            compile_kwargs={"literal_binds": True}
        )
    )
    assert claimed_actual_sql == expected_claimed_sql
