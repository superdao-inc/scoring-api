from sqlalchemy import Column, UniqueConstraint
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.types import String

from app.db import Base


class FixedListItem(Base):
    __tablename__ = "fixed_lists"

    list_id = Column(String, primary_key=True, index=True)
    wallet = Column(String, primary_key=True, index=True)
    wallet_b = Column(BYTEA, primary_key=True, index=True)

    __table_args__ = (
        UniqueConstraint(
            "wallet",
            "list_id",
        ),
    )
