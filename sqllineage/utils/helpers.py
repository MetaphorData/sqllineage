import logging
from argparse import Namespace
from typing import Optional

logger = logging.getLogger(__name__)


def escape_identifier_name(name: str):
    return name.strip("`").strip('"').strip("'")


def extract_sql_from_args(args: Namespace) -> str:
    sql = ""
    if getattr(args, "f", None):
        try:
            with open(args.f) as f:
                sql = f.read()
        except IsADirectoryError:
            logger.exception("%s is a directory", args.f)
            exit(1)
        except FileNotFoundError:
            logger.exception("No such file: %s", args.f)
            exit(1)
        except PermissionError:
            # On Windows, open a directory as file throws PermissionError
            logger.exception("Permission denied when reading file '%s'", args.f)
            exit(1)
    elif getattr(args, "e", None):
        sql = args.e
    return sql


def table_fullname(
    table: str, default_database: Optional[str], default_schema: Optional[str]
) -> str:
    """
    Best effort to assemble the table fullname and normalize to lowercase
    If missing database or schema, return the input table name
    """
    dots = table.count(".")
    if dots == 0:
        if default_database and default_schema:
            return f"{default_database}.{default_schema}.{table}".lower()
    elif dots == 1:
        if default_database:
            return f"{default_database}.{table}".lower()

    return table.lower()
