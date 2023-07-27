from typing import Any, Tuple

import sqlalchemy as sa


def create_partition_table(
    partitioned_table: Any,
    partition_name: str,
    partition_bases: Tuple,
    partition_stmt: str,
    partition_table_args: Any,
) -> Any:
    table = type(
        partition_name,
        partition_bases,
        {'__tablename__': partition_name, '__table_args__': partition_table_args},
    )
    table.__table__.add_is_dependent_on(partitioned_table)  # type: ignore

    attach_partition_ddl = sa.DDL(  # type: ignore
        f"""
        ALTER TABLE {partitioned_table.name} ATTACH PARTITION {partition_name}
        {partition_stmt};
        """
    )
    sa.event.listen(
        table.__table__, 'after_create', attach_partition_ddl  # type: ignore
    )

    return table


class PartitionsMeta(type):
    def __init__(cls: "BasePartitions", *args, **kwargs):  # type: ignore
        for partition_name in cls.partitions_names:
            cls.partitions_models.append(
                create_partition_table(
                    cls.partitioned_table,
                    f'{cls.partitioned_table.name}_{partition_name}',
                    cls.partition_bases,
                    cls.build_partition_stmt(partition_name),
                    cls.partition_table_args,
                )
            )


class BasePartitions(metaclass=PartitionsMeta):
    '''
    Base class for creating partitions for partitioned table.
    Works only with LIST partitioning.

    Assumes that partitions names are partitions keys values.
    For example, if partition name is `0x1`, then
    partition key value should be `0x1`.

    If partition name is `DEFAULT_PARTION_NAME`,
    then it will be used as default partition.
    '''

    DEFAULT_PARTION_NAME = 'default'

    partitioned_table: Any
    partition_bases: Tuple
    partition_table_args: Any
    partitions_names: list[str] = []

    partitions_models: list[Any] = []

    @classmethod
    def build_partition_stmt(cls, partition_name: str) -> str:
        if partition_name == cls.DEFAULT_PARTION_NAME:
            return "DEFAULT"

        return f"FOR VALUES IN ('{partition_name}')"
