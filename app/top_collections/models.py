import sqlalchemy as sa
from sqlalchemy import Column, Index, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.types import TIMESTAMP, Integer, String

from app.common.enums import AudienceType, BlockchainType
from app.db import Base


class TopCollectionsBaseModel(Base, AbstractConcreteBase):
    __abstract__ = True
    strict_types = True

    chain = Column(
        ENUM(BlockchainType, name='blockchaintype'),
        name="chain",
        primary_key=True,
        nullable=False,
    )
    audience_slug = Column(
        String, name="audience_slug", primary_key=True, index=True, nullable=False
    )
    audience_type = Column(
        ENUM(AudienceType, name='audiencetype'),
        name="audience_type",
        primary_key=True,
        index=True,
        nullable=False,
    )
    token_address = Column(
        String, name="token_address", primary_key=True, index=True, nullable=False
    )
    nft_count = Column(Integer, name="nft_count", nullable=False)
    holders_count = Column(Integer, name="holders_count", nullable=True)
    total_nft_count = Column(Integer, name="total_nft_count", nullable=True)
    total_holders_count = Column(Integer, name="total_holders_count", nullable=True)
    updated = Column(TIMESTAMP, name="updated", nullable=False, default=sa.func.now())


class TopCollectionsModel(TopCollectionsBaseModel):
    __tablename__ = 'top_collections'
    __mapper_args__ = {
        "concrete": True,  # for inheritance
    }

    __table_args__ = (
        UniqueConstraint(
            TopCollectionsBaseModel.chain.name,
            TopCollectionsBaseModel.audience_slug.name,
            TopCollectionsBaseModel.audience_type.name,
            TopCollectionsBaseModel.token_address.name,
            name='top_collections_chain_audience_slug_audience_type_token_add_key',
        ),
        Index(
            'idx_top_collections_audience_slug_audience_type_holders_count',
            TopCollectionsBaseModel.audience_slug.name,
            TopCollectionsBaseModel.audience_type.name,
            TopCollectionsBaseModel.holders_count.name,
        ),
        Index(
            'idx_top_collections_audience_slug_audience_type_nft_count',
            TopCollectionsBaseModel.audience_slug.name,
            TopCollectionsBaseModel.audience_type.name,
            TopCollectionsBaseModel.nft_count.name,
        ),
    )


class TopWhitelistedCollectionsModel(TopCollectionsBaseModel):
    __tablename__ = 'top_whitelisted_collections'
    __mapper_args__ = {
        "concrete": True,  # for inheritance,
    }

    __table_args__ = (
        PrimaryKeyConstraint(
            "chain",
            "audience_slug",
            "audience_type",
            "token_address",
            name='top_whitelisted_collections_pkey',
        ),
        Index(
            'idx_top_whitelisted_collections_slug_type_holders',
            TopCollectionsBaseModel.audience_slug.name,
            TopCollectionsBaseModel.audience_type.name,
            TopCollectionsBaseModel.holders_count.name,
        ),
        Index(
            'idx_top_whitelisted_collections_slug_type_nft_count',
            TopCollectionsBaseModel.audience_slug.name,
            TopCollectionsBaseModel.audience_type.name,
            TopCollectionsBaseModel.nft_count.name,
        ),
    )
