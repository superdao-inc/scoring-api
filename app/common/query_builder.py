import abc
from datetime import datetime
from typing import Any, List, Optional, Tuple

import sqlalchemy as sa
from eth_utils import is_address

from app.common.helpers import address_to_bytea, get_model_column, parse_interval_bucket
from app.nft_holders.models import NftHolders
from app.wallet.models import WalletAttributes
from app.wallet.query_builder import WalletQueryBuilder


class AbstractWalletAttributesQueryBuilder(abc.ABC):
    attributes_model = WalletAttributes
    attributes_model_wallet_address_column: Any = WalletAttributes.wallet

    left_model: Any
    left_model_wallet_address_column: Any
    left_model_order_columns: List[Any]
    left_model_searchable_columns: List[Any]

    @classmethod
    @abc.abstractmethod
    def build_order_expressions(
        cls, fields: List[str], direction: Optional[str]
    ) -> List[sa.UnaryExpression]:
        order_expressions: List[sa.UnaryExpression] = []

        if fields:
            for field in fields:
                # optimize order by wallet
                if cls.attributes_model == WalletAttributes and field == 'wallet':
                    field = 'wallet_b'

                column = get_model_column(field, cls.left_model, cls.attributes_model)
                order_expressions.append(
                    sa.desc(column).nulls_last()
                    if direction == "DESC"
                    else sa.asc(column).nulls_last()
                )

        for c in cls.left_model_order_columns:
            order_expressions.append(c)

        order_expressions.append(
            (
                cls.left_model_wallet_address_column
                or cls.attributes_model_wallet_address_column
            ).asc()
        )

        return order_expressions

    @classmethod
    @abc.abstractmethod
    def get_join_clause(cls) -> sa.Join:
        return sa.join(
            cls.left_model,
            cls.attributes_model,
            cls.left_model_wallet_address_column
            == cls.attributes_model_wallet_address_column,
            isouter=False,
        )

    @classmethod
    @abc.abstractmethod
    def build_base_where_clauses(
        cls,
        where_field: Optional[str],
        where_operator: Optional[str],
        where_values: Optional[List[str]],
    ) -> List[sa.ColumnElement[bool]]:
        clauses = []

        if where_field and where_operator and where_values:
            column = get_model_column(where_field, cls.left_model, cls.attributes_model)
            if column.type.python_type != list:
                where_values = [
                    column.type.python_type(v) if v is not None else None
                    for v in where_values
                ]
            if where_operator == "contains":
                # all passed must be included
                clauses.append(column.contains(where_values))
            elif where_operator == "overlap":
                # one of passed must be included
                clauses.append(column.bool_op('&&')(where_values))
            elif where_operator == "ne":
                for where_value in where_values:
                    clauses.append(column != where_value)
            elif where_operator == "eq":
                for where_value in where_values:
                    clauses.append(column == where_value)
            else:
                raise ValueError("Invalid operator")

        return clauses

    @classmethod
    @abc.abstractmethod
    def build_base_where_clause(
        cls,
        *args: Any,
        custom_where_clauses: List[Any],
        where_field: Optional[str],
        where_operator: Optional[str],
        where_values: Optional[List[str]],
        **kwargs: Any,
    ) -> sa.ColumnElement[bool]:
        clauses = cls.build_base_where_clauses(
            where_field, where_operator, where_values
        )

        return sa.and_(*custom_where_clauses, *clauses)

    @classmethod
    @abc.abstractmethod
    def build_search_where_clause(
        cls, pattern: Optional[str]
    ) -> sa.ColumnElement[bool]:
        if pattern:
            clauses = [
                sa.func.lower(c).contains(pattern.lower())
                for c in cls.left_model_searchable_columns
            ]
            return sa.or_(
                *clauses,
                *WalletQueryBuilder.build_search_where_clauses(
                    pattern, not cls.left_model
                ),
            )

        return sa.true()

    @classmethod
    @abc.abstractmethod
    def build_aggregation_query(
        cls, custom_where_clauses: List[Any], request: Any
    ) -> sa.Select[Any]:
        if request.agg_type == "count":
            query = sa.select(
                sa.func.count(
                    get_model_column(
                        request.agg_field, cls.left_model, cls.attributes_model
                    )
                )
            )
        elif request.agg_type == "sum":
            query = sa.select(
                sa.func.sum(
                    get_model_column(
                        request.agg_field, cls.left_model, cls.attributes_model
                    )
                )
            )
        elif request.agg_type == "count_bucket_intervals":
            query = cls.build_count_bucket_intervals_aggregation_query(request)
        elif request.agg_type == "count_bucket_values":
            query = cls.build_count_bucket_values_aggregation_query(request)
        else:
            raise ValueError("Invalid aggregation type")

        if cls.left_model is None:
            query = query.select_from(cls.attributes_model)
        else:
            query = query.select_from(cls.get_join_clause())

        query = query.where(
            cls.build_base_where_clause(
                custom_where_clauses=custom_where_clauses,
                where_field=request.where_field,
                where_operator=request.where_operator,
                where_values=request.where_values,
            )
        ).where(cls.build_search_where_clause(request.search))

        return (
            cls.append_overlap_clause(
                query,
                cls.left_model_wallet_address_column
                or cls.attributes_model_wallet_address_column,
                request.overlap_audiences,
            )
            if request.overlap_audiences
            else query
        )

    @classmethod
    @abc.abstractmethod
    def build_count_bucket_intervals_aggregation_query(
        cls, request: Any
    ) -> sa.Select[Any]:
        if not request.buckets:
            raise ValueError("Buckets are required for count_bucket_intervals")

        model_column = get_model_column(
            request.agg_field, cls.left_model, cls.attributes_model
        )
        ifnull_value = 0
        select_clause = []
        for bucket in request.buckets:
            from_, to_ = parse_interval_bucket(bucket)
            if model_column.type.python_type == datetime:
                from_ = datetime.fromtimestamp(from_) if from_ else None  # type: ignore
                to_ = datetime.fromtimestamp(to_) if to_ else None  # type: ignore
                ifnull_value = datetime.fromtimestamp(0)  # type: ignore
            column = sa.sql.func.coalesce(model_column, ifnull_value)
            f = sa.func.count(column)
            if from_ is not None:
                f = f.filter(column >= from_)  # type: ignore
            if to_ is not None:
                f = f.filter(column <= to_)  # type: ignore
            select_clause.append(f)

        return sa.select(*select_clause)

    @classmethod
    @abc.abstractmethod
    def build_count_bucket_values_aggregation_query(
        cls, request: Any
    ) -> sa.Select[Any]:
        if not request.buckets:
            raise ValueError("Buckets are required for count_bucket_values")

        column = get_model_column(
            request.agg_field, cls.left_model, cls.attributes_model
        )

        if column.type.python_type == list:

            def get_function_filter(value: Any) -> sa.SQLColumnExpression[Any]:
                return column.contains(value)

        elif column.type.python_type in [str, int]:

            def get_function_filter(value: Any) -> sa.SQLColumnExpression[Any]:
                return column == value

        else:
            raise ValueError(f"Invalid aggregation field: {request.agg_field}")

        select_clause = []
        for bucket in request.buckets:
            if column.type.python_type == list:
                bucket = [bucket]

            c = sa.func.count(column).filter(
                get_function_filter(bucket)
            )  # type: ignore
            select_clause.append(c)

        return sa.select(*select_clause)

    @classmethod
    @abc.abstractmethod
    def build_total_count_query(
        cls, custom_where_clauses: List[Any], request: Any
    ) -> sa.Select[Any]:
        if cls.left_model is None:
            query = sa.select(sa.func.count(cls.attributes_model_wallet_address_column))
        else:
            query = sa.select(
                sa.func.count(cls.left_model_wallet_address_column)
            ).select_from(cls.get_join_clause())

        query = (
            cls.append_overlap_clause(
                query,
                cls.left_model_wallet_address_column
                or cls.attributes_model_wallet_address_column,
                request.overlap_audiences,
            )
            if request.overlap_audiences
            else query
        )

        query = query.where(
            cls.build_base_where_clause(
                custom_where_clauses=custom_where_clauses,
                where_field=request.where_field,
                where_operator=request.where_operator,
                where_values=request.where_values,
            )
        )
        query = query.where(cls.build_search_where_clause(request.search))

        return query

    @classmethod
    @abc.abstractmethod
    def build_query(
        cls, custom_where_clauses: List[Any], request: Any
    ) -> sa.Select[Any]:
        if cls.left_model is None:
            query = sa.select(cls.attributes_model)
        else:
            query = sa.select(cls.left_model, cls.attributes_model).select_from(
                cls.get_join_clause()
            )

        query = (
            cls.append_overlap_clause(
                query,
                cls.left_model_wallet_address_column
                or cls.attributes_model_wallet_address_column,
                request.overlap_audiences,
            )
            if request.overlap_audiences
            else query
        )

        query = query.where(
            cls.build_base_where_clause(
                custom_where_clauses=custom_where_clauses,
                where_field=request.where_field,
                where_operator=request.where_operator,
                where_values=request.where_values,
            )
        )
        query = query.where(cls.build_search_where_clause(request.search))
        query = query.order_by(
            *cls.build_order_expressions(
                request.order_by_fields, request.order_by_direction
            )
        )

        # Add one to the limit to determine if there are more results
        query = query.offset(request.offset).limit(request.limit + 1)

        return query

    @classmethod
    @abc.abstractmethod
    def append_overlap_clause(
        cls,
        query: sa.Select,
        address_column: Any,
        overlap_collections: List[str],
    ) -> sa.Select:
        def _parse_audience(audience: str) -> Tuple[str, bool]:
            if audience.startswith('-'):
                return audience[1:], False

            return audience, True

        for collection in overlap_collections:
            contract, sign = _parse_audience(collection)
            if not is_address(contract):
                continue

            partition_key = contract[:3]
            subquery = sa.select(address_to_bytea(NftHolders.wallet)).where(
                sa.and_(
                    NftHolders.contract_prefix == partition_key,
                    NftHolders.token_contract == contract,
                )
            )

            in_ = address_column.in_ if sign else address_column.notin_
            query = query.where(in_(subquery))

        return query
