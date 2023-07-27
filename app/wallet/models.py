from typing import List

import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ARRAY, BYTEA
from sqlalchemy.types import TIMESTAMP, BigInteger, Integer, String

from app.db import Base


class WalletAttributes(Base):
    __tablename__ = "wallet_attributes"

    wallet = Column(String, nullable=False, primary_key=True)
    wallet_b = Column(BYTEA, nullable=False)
    created_at = Column(TIMESTAMP)
    ens_name = Column(String)
    email = Column(String)
    labels = Column(ARRAY(String))
    last_month_tx_count = Column(Integer)
    last_month_in_volume = Column(Integer)
    last_month_out_volume = Column(Integer)
    last_month_volume = Column(Integer)
    nfts_count = Column(Integer)
    twitter_avatar_url = Column(String)
    twitter_followers_count = Column(Integer)
    twitter_url = Column(String)
    twitter_username = Column(String)
    twitter_location = Column(String)
    twitter_bio = Column(String)
    tx_count = Column(Integer)
    wallet_usd_cap = Column(BigInteger)
    whitelist_activity = Column(ARRAY(String))
    superrank = Column(Integer)

    labels_values = [
        'whale',
        'voter',
        'influencer',
        'hunter',
        'nonhuman',
        'audience:culture:art',
        'audience:culture:fasion',
        'audience:culture:music',
        'audience:culture:luxury',
        'audience:defi',
        'audience:developers',
        'audience:donor',
        'audience:early_adopters',
        'audience:gaming',
        'audience:investor',
        'audience:professional',
        'nft_trader',
        'passive',
        'zombie',
    ]
    orderable_columns = [
        'created_at',
        'nfts_count',
        'twitter_followers_count',
        'wallet_usd_cap',
        'superrank',
    ]

    # lookup index
    lookup_index = sa.Index('ix_wa__wallet', 'wallet')

    # indices for label queries
    label_partial_indices: List[sa.Index] = []
    for i, label in enumerate(labels_values, start=1):
        for j, column in enumerate(orderable_columns, start=1):
            for direction in ['ASC', 'DESC']:
                ix_name = f'ix_wa__label_{i}__column_{j}_{direction}'
                ix_expression = sa.text(f'{column} {direction} NULLS LAST')
                ix_predicate = sa.text(f"labels @> '{{{label}}}'::varchar[];")
                ix = sa.Index(ix_name, ix_expression, postgresql_where=ix_predicate)

                label_partial_indices.append(ix)

    # indices for join queries
    column_indices: List[sa.Index] = []
    for j, column in enumerate(orderable_columns, start=1):
        for direction in ['ASC', 'DESC']:
            ix_name = f'ix_wa__column_{j}_{direction}_wallet_b'
            ix_expressions = [
                sa.text(f'{column} {direction} NULLS LAST'),
                sa.text('wallet_b'),
            ]
            ix = sa.Index(ix_name, *ix_expressions)

            column_indices.append(ix)

    # search index
    search_indices = [
        sa.Index(
            'ix_wa__search__wallet_ens_name_lower',
            sa.func.lower('ens_name'),
            sa.func.lower('wallet'),
        )
    ]

    __table_args__ = (
        lookup_index,
        *label_partial_indices,
        *column_indices,
        *search_indices,
    )
