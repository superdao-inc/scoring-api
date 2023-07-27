from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.types import String

from app.common.partitioned import BasePartitions
from app.db import Base


class NftHoldersMixin:
    contract_prefix = Column(String, nullable=False)
    token_contract = Column(String, nullable=False)
    wallet = Column(String, nullable=False)
    wallet_b = Column(BYTEA, nullable=False)


class NftHolders(NftHoldersMixin, Base):
    __tablename__ = "nft_holders"
    __table_args__ = (
        PrimaryKeyConstraint(
            'contract_prefix', 'token_contract', 'wallet_b', name='nft_holders_pkey'
        ),
        {'postgresql_partition_by': 'LIST (contract_prefix)'},
    )


class NftHoldersPartitions(BasePartitions):
    partitioned_table = NftHolders.__table__
    partition_bases = (NftHoldersMixin, Base)
    partition_table_args = (
        PrimaryKeyConstraint('contract_prefix', 'token_contract', 'wallet_b'),
    )
    partitions_names = [
        '0x0',
        '0x1',
        '0x2',
        '0x3',
        '0x4',
        '0x5',
        '0x6',
        '0x7',
        '0x8',
        '0x9',
        '0xa',
        '0xb',
        '0xc',
        '0xd',
        '0xe',
        '0xf',
    ]
