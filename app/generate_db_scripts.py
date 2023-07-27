"""
To speed up the deployment of the database, we use a three-step approach:
1. Create all tables without indices and constraints
2. Insert all data
3. Create all indices and constraints

To achieve this, we generate full database schema via SQLAlchemy
and dump it into a file. Then we parse this file and devide it into two parts:
tables and indices/constraints.
Then we use these two parts to generate two scripts: step_1.sql and step_2.sql.
We use theese scripts on CI/CD to speed up the deployment of the database.
"""

import os
import re
import subprocess  # nosec

import sqlalchemy as sa
import testing.postgresql
from pglast import ast, enums, parse_sql
from pglast.stream import IndentedStream

from app.analytics.models import *  # noqa: F401, F403
from app.claimed.models import *  # noqa: F401, F403
from app.db import Base
from app.dictionary.models import *  # noqa: F401, F403
from app.fixed_list.models import *  # noqa: F401, F403
from app.inputs.models import *  # noqa: F401, F403
from app.nft_holders.models import *  # noqa: F401, F403
from app.top_collections.models import *  # noqa: F401, F403
from app.wallet.models import *  # noqa: F401, F403


def main() -> None:
    # create test db and create all models
    db = testing.postgresql.Postgresql()
    engine = sa.create_engine(db.url())
    Base.metadata.create_all(engine)

    # dump database schema
    dump_path = os.path.join(os.path.dirname(__file__), "dump.sql")

    command = f"""
    pg_dump \
        -h {db.dsn()['host']} \
        -p {db.dsn()['port']} \
        -d {db.dsn()['database']} \
        -U {db.dsn()['user']} \
        --schema-only --no-comments --no-acl --no-owner > {dump_path}
        """

    subprocess.run(command, shell=True, check=True)  # nosec

    # devide dump into two parts: tables and indices/constraints
    with open(dump_path, "r") as f:
        sql = f.read()

    step_1_nodes = []  # tables without indices and constraints
    step_2_nodes = []  # indices and constraints

    parsed_sql = parse_sql(sql)
    for node in parsed_sql:
        if isinstance(node, ast.IndexStmt):
            step_2_nodes.append(node)
            continue

        elif isinstance(node, ast.RawStmt):
            if isinstance(node.stmt, ast.VariableSetStmt):
                continue

            elif isinstance(node.stmt, ast.SelectStmt):
                continue

            elif isinstance(node.stmt, ast.AlterTableStmt):
                if node.stmt.objtype == enums.ObjectType.OBJECT_INDEX:
                    step_2_nodes.append(node)
                    continue
                elif node.stmt.cmds[0].subtype == enums.AlterTableType.AT_AddConstraint:
                    step_2_nodes.append(node)
                    continue

            elif isinstance(node.stmt, ast.IndexStmt):
                step_2_nodes.append(node)
                continue

        step_1_nodes.append(node)

    with open(
        os.path.join(os.path.dirname(__file__), os.pardir, "scripts", "step_1.sql"), "w"
    ) as f:
        f.write(IndentedStream()(tuple(step_1_nodes)))

    with open(
        os.path.join(os.path.dirname(__file__), os.pardir, "scripts", "step_2.sql"), "w"
    ) as f:
        f.write(IndentedStream()(tuple(step_2_nodes)))

    # remove test db dump file
    os.remove(dump_path)

    # bumb db_version.yml
    # read db_version.yml from parent directory
    with open(
        os.path.join(os.path.dirname(__file__), os.pardir, "db_version.yml"), "r"
    ) as f:
        content = f.read()

    version = int(re.findall(r'DB_VERSION: "(\d+)"', content)[0])
    content = content.replace(
        f"DB_VERSION: \"{version}\"", f"DB_VERSION: \"{version + 1}\""
    )

    with open(
        os.path.join(os.path.dirname(__file__), os.pardir, "db_version.yml"), "w"
    ) as f:
        f.write(content)


if __name__ == "__main__":
    main()
