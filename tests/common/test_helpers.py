import pytest

from contextlib import nullcontext as does_not_raise

import sqlalchemy as sa

from app.db import Base

from app.common.helpers import parse_interval_bucket, get_model_column


@pytest.mark.parametrize(
    "bucket, from_, to_, expectation",
    [
        ("t:100", None, 100, does_not_raise()),
        ("f:100;t:1000", 100, 1000, does_not_raise()),
        ("f:1000", 1000, None, does_not_raise()),
        ("", None, None, does_not_raise()),
        ("t:10;f:100", None, None, pytest.raises(ValueError)),
        ("t:10A", None, None, pytest.raises(ValueError)),
    ],
)
def test_parse_interval_bucket(bucket, from_, to_, expectation):
    with expectation:
        actual_from, actual_to = parse_interval_bucket(bucket)

        assert actual_from == from_
        assert actual_to == to_


class A(Base):
    __tablename__ = 'a'
    pk = sa.Column(sa.Integer, primary_key=True)
    c1 = sa.Column(sa.String)


class B(Base):
    __tablename__ = 'b'
    pk = sa.Column(sa.Integer, primary_key=True)
    c2 = sa.Column(sa.String)


@pytest.mark.parametrize(
    "column_name, models, column, expectation",
    [
        ("c1", [A, B], A.c1, does_not_raise()),
        ("c2", [A, B], B.c2, does_not_raise()),
        ("c3", [A, B], None, pytest.raises(ValueError)),
    ],
)
def test_get_model_column(column_name, models, column, expectation):
    with expectation:
        actual_column = get_model_column(column_name, *models)

        assert actual_column == column
