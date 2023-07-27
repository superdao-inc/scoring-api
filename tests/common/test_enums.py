import pytest

from contextlib import nullcontext as does_not_raise

from app.common.enums import BlockchainType


@pytest.mark.parametrize(
    "v, e, expectation",
    [
        ('eth', BlockchainType.ETHEREUM, does_not_raise()),
        ('ethereum', BlockchainType.ETHEREUM, does_not_raise()),
        ('ETH', BlockchainType.ETHEREUM, does_not_raise()),
        ('ETHEREUM', BlockchainType.ETHEREUM, does_not_raise()),
        ('Ethereum', BlockchainType.ETHEREUM, does_not_raise()),
        ('polygon', BlockchainType.POLYGON, does_not_raise()),
        ('matic', None, pytest.raises(ValueError)),
    ],
)
def test_blockchain_type_enum(v, e, expectation):
    with expectation:
        actual = BlockchainType(v)
        assert actual == e
