from sqlalchemy import Column, func
from sqlalchemy.types import TIMESTAMP, Enum, String

from app.db import Base
from app.dictionary.enums import DictionaryValueType


class DictionaryItem(Base):
    __tablename__ = 'dictionary'

    key = Column(String, primary_key=True)
    value = Column(String, nullable=True)
    value_type = Column(Enum(DictionaryValueType), nullable=False)
    updated = Column(TIMESTAMP, nullable=False, server_default=func.now())
