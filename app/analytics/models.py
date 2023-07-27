import enum

from sqlalchemy import Column, Enum, Integer
from sqlalchemy.types import TIMESTAMP, String

from app.db import Base


class WalletEventsType(enum.Enum):
    WALLET_CONNECT = 'WALLET_CONNECT'
    FORM_SUBMIT = 'FORM_SUBMIT'


class WalletLastEvents(Base):
    __tablename__ = "analytics_wallet_last_events"

    tracker_id = Column(String, primary_key=True, index=True)
    address = Column(String, primary_key=True, index=True)
    last_event = Column(Enum(WalletEventsType), nullable=False, index=True)
    last_event_timestamp = Column(TIMESTAMP, nullable=False)
    source = Column(String, nullable=True)
    updated = Column(TIMESTAMP, nullable=False)


class AnalyticsEventsSources(Base):
    __tablename__ = "analytics_events_sources"

    tracker_id = Column(String, primary_key=True, nullable=False)
    event_type = Column(String, primary_key=True, nullable=False)
    source = Column(String, primary_key=True, nullable=False)
    count = Column(Integer, nullable=False)


class AnalyticsEventsCounts(Base):
    __tablename__ = "analytics_events_counts"

    tracker_id = Column(String, primary_key=True, nullable=False)
    event_type = Column(String, primary_key=True, nullable=False, index=True)
    timestamp = Column(TIMESTAMP, primary_key=True, nullable=False, index=True)
    count = Column(Integer, nullable=False)
