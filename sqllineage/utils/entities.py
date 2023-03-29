from typing import NamedTuple, Optional

from sqlparse.sql import Parenthesis, Token


class SubQueryTuple(NamedTuple):
    parenthesis: Parenthesis
    alias: str


class ColumnQualifierTuple(NamedTuple):
    column: str
    qualifier: Optional[str]
    fullname: Optional[str] = None


class ColumnExpression(NamedTuple):
    is_identity: bool
    token: Optional[Token]
