from typing import Any, List, Optional

import sqlalchemy as sa

from app.common.helpers import get_model_column
from app.wallet.models import WalletAttributes


class WalletQueryBuilder:
    @classmethod
    def build_attributes_query(cls, wallet: str) -> sa.Select:
        wallet_hex = wallet[2:]
        return sa.select(WalletAttributes).where(
            WalletAttributes.wallet_b == sa.func.decode(wallet_hex, 'hex')
        )

    @classmethod
    def build_search_where_clauses(
        cls, pattern: Optional[str], include_address: bool
    ) -> List:
        if not pattern:
            return []

        clauses = [
            sa.func.lower(WalletAttributes.ens_name).contains(pattern.lower()),
            # temporary disabled because of performance issues
            # sa.func.lower(WalletAttributes.twitter_username).contains(
            #     pattern.lower()
            # ),
        ]

        if include_address:
            clauses.append(
                sa.func.lower(WalletAttributes.wallet).contains(pattern.lower())
            )

        return clauses

    @classmethod
    def build_leaderboard_query(
        cls, fields: Optional[Any], direction: Optional[str], limit: Optional[int]
    ) -> sa.Select:
        order_expressions: List[sa.UnaryExpression] = []

        if fields:
            for field in fields:
                column = get_model_column(field, WalletAttributes)
                order_expressions.append(
                    sa.desc(column).nulls_last()
                    if direction == "DESC"
                    else sa.asc(column).nulls_last()
                )

        order_expressions.append(WalletAttributes.wallet_b.asc())

        return sa.select(WalletAttributes).order_by(*order_expressions).limit(limit)

    @classmethod
    def build_similar_wallets_attributes_query(
        cls, wallets: List[str], limit: Optional[int]
    ) -> sa.Select:
        return (
            sa.select(WalletAttributes)
            .where(WalletAttributes.wallet.in_(wallets))
            .order_by(
                WalletAttributes.superrank.desc().nulls_last(),
                WalletAttributes.wallet_b.asc(),
            )
            .limit(limit)
        )
