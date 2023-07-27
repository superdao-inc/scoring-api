from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.types import String

from app.db import Base


class ActivityMetadata(Base):
    __tablename__ = 'input_activity_metadata'

    address = Column(String, primary_key=True, index=True)
    chain = Column(
        ENUM(
            'ETHEREUM',
            'POLYGON',
            name='blockchaintype',
            create_type=False,
        ),
        nullable=True,
    )
    name = Column(String, nullable=False)
    external_url = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
