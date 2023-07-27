import enum
import re
from datetime import datetime
from typing import Any, Optional, Tuple, Union

import sqlalchemy as sa
from dateutil.relativedelta import relativedelta

from app.audience.schemas import AudienceItem
from app.claimed.schemas import ClaimedItem
from app.common.schemas import CSVExportColumn
from app.fixed_list.schemas import FixedListItem

BUCKET_REGEX = re.compile(r"^(?:f:(\d+);?)?(?:t:(\d+))?$")


def parse_interval_bucket(bucket: str) -> Tuple[Optional[int], Optional[int]]:
    match = re.match(BUCKET_REGEX, bucket)
    if not match:
        raise ValueError("Invalid bucket format")

    from_ = match.group(1)
    from_ = int(from_) if from_ else None
    to_ = match.group(2)
    to_ = int(to_) if to_ else None

    return from_, to_


def export_item_attrs_to_csv(
    item: Union[AudienceItem, ClaimedItem, FixedListItem], fields: list[CSVExportColumn]
) -> list[str]:
    result = []
    for f in fields:
        if hasattr(item, f.key):
            attr = getattr(item, f.key)

            if attr is None:
                attr = ''

            elif f.key == 'created_at':
                dt = datetime.fromtimestamp(int(attr))
                attr = dt.isoformat()

            elif f.key == 'superrank':
                attr = str(int(attr))

            elif isinstance(attr, list):
                attr = ",".join(attr)

            elif isinstance(attr, enum.Enum):
                attr = attr.value

            result.append(attr)

        elif f.key == 'wallet_age':
            if item.created_at:
                dt = datetime.fromtimestamp(int(item.created_at))
                attr = calculate_date_diff(dt, datetime.now())
                result.append(attr)
            else:
                result.append("")

    return result


def get_model_column(column_name: str, *models: Any) -> sa.Column:
    for model in models:
        if model and column_name in model.__table__.columns:
            c = getattr(model, column_name)
            return c

    raise ValueError(f"Invalid field name: {column_name}")


def address_to_bytea(column: Any) -> sa.Function:
    return sa.func.decode(sa.func.substring(column, 3), 'hex')


def calculate_date_diff(date1: datetime, date2: datetime) -> str:
    diff = relativedelta(date2, date1)

    parts = []
    if diff.years > 0:
        parts.append(f"{diff.years}y")
    if diff.months > 0:
        parts.append(f"{diff.months}m")
    if diff.days > 0:
        parts.append(f"{diff.days}d")

    return " ".join(parts)
