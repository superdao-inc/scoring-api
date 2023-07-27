from sqlalchemy import Column, Enum, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.types import String

from app.common.enums import BlockchainType
from app.common.partitioned import BasePartitions
from app.db import Base


class ClaimedMixin:
    wallet = Column(String, nullable=False)
    wallet_b = Column(BYTEA)
    blockchain = Column(Enum(BlockchainType), nullable=False)
    claimed_contract = Column(String, nullable=False)


class Claimed(ClaimedMixin, Base):
    __tablename__ = "claimed"
    __table_args__ = (
        PrimaryKeyConstraint(
            'claimed_contract', 'wallet_b', 'blockchain', name='claimed_pkey'
        ),
        {'postgresql_partition_by': 'LIST (claimed_contract)'},
    )


class ClaimedPartitions(BasePartitions):
    partitioned_table = Claimed.__table__
    partition_bases = (ClaimedMixin, Base)
    partition_table_args = (
        PrimaryKeyConstraint('claimed_contract', 'wallet_b', 'blockchain'),
    )
    partitions_names = [
        BasePartitions.DEFAULT_PARTION_NAME,
        '0x514910771af9ca656af840dff83e8264ecf986ca',
        '0xa9a6a3626993d487d2dbda3173cf58ca1a9d9e9f',
        '0x6b175474e89094c44da98b954eedeac495271d0f',
        '0x1871464f087db27823cff66aa88599aa4815ae95',
        '0xd26114cd6ee289accf82350c8d8487fedb8a0c07',
        '0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85',
        '0x0d8775f648430679a709e98d2b0cb6250d2887ef',
        '0x1f9840a85d5af5bf1d1762f925bdaddc4201f984',
        '0x0f5d2fb29fb7d3cfee444a200298f468908cc942',
        '0x0d500b1d8e8ef31e21c99d1db9a6444d3adf1270',
        '0xf3e014fe81267870624132ef3a646b8e83853a96',
        '0x1a13f4ca1d028320a707d99520abfefca3998b7f',
        '0xe41d2489571d322189246dafa5ebde1f4699f498',
        '0x92e52a1a235d9a103d970901066ce910aacefd37',
        '0x3845badade8e6dff049820680d1f14bd3903a5d0',
        '0x2b591e99afe9f32eaa6214f7b7629768c40eeb39',
        '0x8df3aad3a84da6b69a4da8aec3ea40d9091b2ac4',
        '0xb8c77482e45f1f44de1745f52c74426c631bdd52',
        '0xf629cbd94d3791c9250152bd8dfbdf380e2a3b9c',
        '0xa0b73e1ff0b80914ab6fe0444e65848c4c34450b',
        '0xd6df932a45c0f255f85145f286ea0b292b21c90b',
        '0xe530441f4f73bdb6dc2fa5af7c3fc5fd551ec838',
        '0x28424507fefb6f7f8e9d3860f56504e4e5f5f390',
        '0x4dc3643dbc642b72c158e7f3d2ff232df61cb6ce',
        '0x8a953cfe442c5e8855cc6c61b1293fa648bae472',
        '0xe06bd4f5aac8d0aa337d13ec88db6defc6eaeefe',
        '0xc944e90c64b2c07662a292be6244bdf05cda44a7',
        '0xc00e94cb662c3520282e6f5717214004a7f26888',
        '0x4092678e4e78230f46a1534c0fbc8fa39780892b',
        '0x89d24a6b4ccb1b6faa2625fe562bdd9a23260359',
        '0x111111111117dc0aa78b770fa6a738034120c302',
        '0x6b3595068778dd592e39a122f4f5a5cf09c90fe2',
        '0x4e15361fd6b4bb609fa63c81a2be19d873717870',
        '0xbbbbca6a901c926f240b89eacb641d8aec7aeafd',
        '0x4d224452801aced8b2f0aebe155379bb5d594381',
        '0x3506424f91fd33084466f402d5d97f05f8e3b4af',
        '0xc011a73ee8576fb46f5e1c5751ca3b9fe0af2a6f',
        '0x6982508145454ce325ddbe47a25d4ec3d2311933',
        '0xd1d2eb1b1e90b638588728b4130137d262c87cae',
        '0xd533a949740bb3306d119cc777fa900ba034cd52',
        '0xf4d2888d29d722226fafa5d9b24f9164c092421e',
        '0x1bfd67037b42cf73acf2047067bd4f2c47d9bfd6',
        '0x60d55f02a771d515e077c9c2403a1ef324885cec',
        '0x4a220e6096b25eadb88358cb44068a3248254675',
        '0x385eeac5cb85a38a9a07a70c73e0a3271cfb54a7',
    ]
