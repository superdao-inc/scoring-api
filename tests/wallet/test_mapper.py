import datetime
from unittest.mock import MagicMock
import pytest

from app.wallet.models import WalletAttributes
from app.wallet.mapper import WalletItemMapper
from app.wallet.schemas import WalletAttributesItem


class MockItem:
    pass


@pytest.fixture
def mapper():
    return WalletItemMapper


@pytest.fixture
def attributes_obj():
    return WalletAttributes(
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
        last_month_in_volume=5,
        last_month_out_volume=15,
        last_month_volume=20,
        wallet_usd_cap=1,
        whitelist_activity=['0xC'],
        superrank=100,
    )


@pytest.fixture
def mock_item():
    return MockItem()


def test_map_wallet_attributes_to(mapper, attributes_obj, mock_item):
    result = mapper.map_wallet_attributes_to(attributes_obj, mock_item)

    assert isinstance(result, MockItem)

    assert result.superrank == attributes_obj.superrank
    assert result.created_at == attributes_obj.created_at.timestamp()
    assert result.tx_count == attributes_obj.tx_count
    assert result.last_month_tx_count == attributes_obj.last_month_tx_count
    assert result.nfts_count == attributes_obj.nfts_count
    assert result.ens_name == attributes_obj.ens_name
    assert result.twitter_url == attributes_obj.twitter_url
    assert result.twitter_username == attributes_obj.twitter_username
    assert result.twitter_avatar_url == attributes_obj.twitter_avatar_url
    assert result.twitter_followers_count == attributes_obj.twitter_followers_count
    assert result.twitter_location == attributes_obj.twitter_location
    assert result.twitter_bio == attributes_obj.twitter_bio
    assert result.wallet_usd_cap == attributes_obj.wallet_usd_cap
    assert result.labels == attributes_obj.labels
    assert result.whitelist_activity == attributes_obj.whitelist_activity


def test_map_to_attributes_item(mapper, attributes_obj):
    mocked_row = MagicMock()
    mocked_row.WalletAttributes = attributes_obj
    result = mapper.map_to_attributes_item(mocked_row)

    assert isinstance(result, WalletAttributesItem)

    assert result.superrank == attributes_obj.superrank
    assert result.created_at == attributes_obj.created_at.timestamp()
    assert result.tx_count == attributes_obj.tx_count
    assert result.last_month_tx_count == attributes_obj.last_month_tx_count
    assert result.nfts_count == attributes_obj.nfts_count
    assert result.ens_name == attributes_obj.ens_name
    assert result.twitter_url == attributes_obj.twitter_url
    assert result.twitter_username == attributes_obj.twitter_username
    assert result.twitter_avatar_url == attributes_obj.twitter_avatar_url
    assert result.twitter_followers_count == attributes_obj.twitter_followers_count
    assert result.twitter_location == attributes_obj.twitter_location
    assert result.twitter_bio == attributes_obj.twitter_bio
    assert result.wallet_usd_cap == attributes_obj.wallet_usd_cap
    assert result.labels == attributes_obj.labels
    assert result.whitelist_activity == attributes_obj.whitelist_activity


def test_map_default_values(mapper, mock_item):
    result = mapper.map_wallet_attributes_to(None, mock_item)

    assert isinstance(result, MockItem)

    assert result.superrank == 0
    assert result.tx_count == 0
    assert result.last_month_tx_count == 0
    assert result.last_month_in_volume == 0
    assert result.last_month_out_volume == 0
    assert result.last_month_volume == 0
    assert result.nfts_count == 0
    assert result.wallet_usd_cap == 0
