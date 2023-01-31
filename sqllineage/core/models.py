import logging
import warnings
from typing import Dict, List, NamedTuple, Optional, Set, Union

from sqlparse import tokens as T
from sqlparse.engine import grouping
from sqlparse.keywords import is_keyword
from sqlparse.sql import (
    Case,
    Comparison,
    Function,
    Identifier,
    IdentifierList,
    Operation,
    Parenthesis,
    Token,
    TokenList,
)

from sqllineage.exceptions import SQLLineageException
from sqllineage.utils.entities import ColumnExpression, ColumnQualifierTuple
from sqllineage.utils.helpers import escape_identifier_name, table_fullname
from sqllineage.utils.schemaFetcher import SchemaFetcher
from sqllineage.utils.sqlparse import (
    get_identifier_name_and_parent,
    get_parameters,
    is_subquery,
)

logger = logging.getLogger(__name__)


class Schema:
    unknown = "<default>"

    def __init__(self, name: str = unknown):
        """
        Data Class for Schema

        :param name: schema name
        """
        self.raw_name = escape_identifier_name(name)

    def __str__(self):
        return self.raw_name.lower()

    def __repr__(self):
        return "Schema: " + str(self)

    def __eq__(self, other):
        return type(self) is type(other) and str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    def __bool__(self):
        return str(self) != self.unknown


class TableMetadata(NamedTuple):
    """
    Data Class for Table metadata used in lineage resolution
    """

    default_database: Optional[str] = None
    default_schema: Optional[str] = None
    platform: Optional[str] = None
    account: Optional[str] = None
    schema_fetcher: Optional[SchemaFetcher] = None

    def get_schema(self, table: str) -> List[str]:
        """
        get table schema using schema fetcher and the other table metadata in this object
        """
        if not self.schema_fetcher:
            return []

        fullname = table_fullname(table, self.default_database, self.default_schema)
        return self.schema_fetcher.get_schema(fullname, self.platform, self.account)


class Table:
    def __init__(self, name: str, schema: Schema = Schema(), **kwargs):
        """
        Data Class for Table

        :param name: table name
        :param schema: schema as defined by :class:`Schema`
        """
        if "." not in name:
            self.schema = schema
            self.raw_name = escape_identifier_name(name)
        else:
            schema_name, table_name = name.rsplit(".", 1)
            if schema_name.count(".") > 1:
                # allow db.schema as schema_name, but a.b.c as schema_name is forbidden
                raise SQLLineageException("Invalid format for table name: %s.", name)
            self.schema = Schema(schema_name)
            self.raw_name = escape_identifier_name(table_name)
            if schema:
                warnings.warn("Name is in schema.table format, schema param is ignored")
        self.alias = kwargs.pop("alias", self.raw_name)

    def __str__(self):
        return f"{self.schema}.{self.raw_name.lower()}"

    def __repr__(self):
        return "Table: " + str(self)

    def __eq__(self, other):
        return type(self) is type(other) and str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    @staticmethod
    def of(identifier: Identifier, metadata=TableMetadata()) -> "Table":
        real_name, parent_name = get_identifier_name_and_parent(identifier)

        if not parent_name:
            if metadata.default_database and metadata.default_schema:
                parent_name = f"{metadata.default_database}.{metadata.default_schema}"
        elif parent_name.count(".") == 0:
            if metadata.default_database:
                parent_name = f"{metadata.default_database}.{parent_name}"

        schema = Schema(parent_name) if parent_name is not None else Schema()
        alias = identifier.get_alias()
        kwargs = {"alias": alias} if alias else {}
        return Table(real_name, schema, **kwargs)


class Path:
    def __init__(self, uri: str):
        self.uri = escape_identifier_name(uri)

    def __str__(self):
        return self.uri

    def __repr__(self):
        return "Path: " + str(self)

    def __eq__(self, other):
        return type(self) is type(other) and self.uri == other.uri

    def __hash__(self):
        return hash(self.uri)


class Partition:
    pass


class SubQuery:
    def __init__(self, token: Parenthesis, alias: Optional[str]):
        """
        Data Class for SubQuery

        :param token: subquery token
        :param alias: subquery name
        """
        self.token = token
        self._query = token.value
        self.alias = alias if alias is not None else f"subquery_{hash(self)}"

    def __str__(self):
        return self.alias

    def __repr__(self):
        return "SubQuery: " + str(self)

    def __eq__(self, other):
        return type(self) is type(other) and self._query == other._query

    def __hash__(self):
        return hash(self._query)

    @staticmethod
    def of(parenthesis: Parenthesis, alias: Optional[str]) -> "SubQuery":
        return SubQuery(parenthesis, alias)


class Column:
    def __init__(self, name: str, **kwargs):
        """
        Data Class for Column

        :param name: column name
        :param parent: :class:`Table` or :class:`SubQuery`
        :param kwargs:
        """
        self._parent: Set[Union[Table, SubQuery]] = set()
        self.raw_name = escape_identifier_name(name)
        self.source_columns: List[ColumnQualifierTuple] = kwargs.pop(
            "source_columns", ((self.raw_name, None),)
        )
        self.expression: ColumnExpression = kwargs.pop(
            "expression", ColumnExpression(True, None)
        )

    def __str__(self):
        return (
            f"{self.parent}.{self.raw_name.lower()}"
            if self.parent is not None and not isinstance(self.parent, Path)
            else f"{self.raw_name.lower()}"
        )

    def __repr__(self):
        return "Column: " + str(self)

    def __eq__(self, other):
        return type(self) is type(other) and str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

    @property
    def parent(self) -> Optional[Union[Table, SubQuery]]:
        return list(self._parent)[0] if len(self._parent) == 1 else None

    @parent.setter
    def parent(self, value: Union[Table, SubQuery]):
        self._parent.add(value)

    @property
    def parent_candidates(self) -> List[Union[Table, SubQuery]]:
        return sorted(self._parent, key=lambda p: str(p))

    @staticmethod
    def of(token: Token):
        if isinstance(token, Identifier):
            alias = token.get_alias()
            if alias:
                # handle column alias, including alias for column name or Case, Function
                kw_idx, kw = token.token_next_by(m=(T.Keyword, "AS"))
                if kw_idx is None:
                    # alias without AS
                    kw_idx, _ = token.token_next_by(i=Identifier)
                if kw_idx is None:
                    # invalid syntax: col AS, without alias
                    return Column(alias)
                else:
                    idx, _ = token.token_prev(kw_idx, skip_cm=True)
                    expr = grouping.group(TokenList(token.tokens[: idx + 1]))[0]
                    source_columns = Column._extract_source_columns(expr)
                    return Column(
                        alias,
                        source_columns=source_columns,
                        expression=ColumnExpression(False, expr),
                    )
            else:
                # select column name directly without alias
                return Column(
                    token.get_real_name(),
                    source_columns=((token.get_real_name(), token.get_parent_name()),),
                    expression=ColumnExpression(True, None),
                )
        else:
            # Wildcard, Case, Function without alias (thus not recognized as an Identifier)
            source_columns = Column._extract_source_columns(token)
            return Column(
                token.value,
                source_columns=source_columns,
                expression=ColumnExpression(False, token),
            )

    @staticmethod
    def _extract_source_columns(token: Token) -> List[ColumnQualifierTuple]:
        if isinstance(token, Function):
            # max(col1) AS col2
            source_columns = [
                cqt
                for tk in get_parameters(token)
                for cqt in Column._extract_source_columns(tk)
            ]
        elif isinstance(token, Parenthesis):
            if is_subquery(token):
                # This is to avoid circular import
                from sqllineage.runner import LineageRunner

                # (SELECT avg(col1) AS col1 FROM tab3), used after WHEN or THEN in CASE clause
                src_cols = [
                    lineage[0]
                    for lineage in LineageRunner(token.value).get_column_lineage(
                        exclude_subquery=False
                    )
                ]
                source_columns = [
                    ColumnQualifierTuple(src_col.raw_name, src_col.parent.raw_name)
                    for src_col in src_cols
                ]
            else:
                # (col1 + col2) AS col3
                source_columns = [
                    cqt
                    for tk in token.tokens[1:-1]
                    for cqt in Column._extract_source_columns(tk)
                ]
        elif isinstance(token, Operation):
            # col1 + col2 AS col3
            source_columns = [
                cqt
                for tk in token.get_sublists()
                for cqt in Column._extract_source_columns(tk)
            ]
        elif isinstance(token, Case):
            # CASE WHEN col1 = 2 THEN "V1" WHEN col1 = "2" THEN "V2" END AS col2
            source_columns = [
                cqt
                for tk in token.get_sublists()
                for cqt in Column._extract_source_columns(tk)
            ]
        elif isinstance(token, Comparison):
            source_columns = Column._extract_source_columns(
                token.left
            ) + Column._extract_source_columns(token.right)
        elif isinstance(token, IdentifierList):
            source_columns = [
                cqt
                for tk in token.get_sublists()
                for cqt in Column._extract_source_columns(tk)
            ]
        elif isinstance(token, Identifier):
            real_name = token.get_real_name()
            # ignore function dtypes that don't need to check for extract column
            FUNC_DTYPE = ["decimal", "numeric"]
            has_function = any(
                isinstance(t, Function) and t.get_real_name() not in FUNC_DTYPE
                for t in token.tokens
            )
            is_kw = is_keyword(real_name) if real_name is not None else False
            if (
                # real name is None: col1=1 AS int
                real_name is None
                # real_name is decimal: case when col1 > 0 then col2 else col3 end as decimal(18, 0)
                or (real_name in FUNC_DTYPE and isinstance(token.tokens[-1], Function))
                or (is_kw and has_function)
            ):
                source_columns = [
                    cqt
                    for tk in token.get_sublists()
                    for cqt in Column._extract_source_columns(tk)
                ]
            else:
                # col1 AS col2
                source_columns = [
                    ColumnQualifierTuple(token.get_real_name(), token.get_parent_name())
                ]
        else:
            if token.ttype == T.Wildcard:
                # select *
                source_columns = [ColumnQualifierTuple(token.value, None)]
            else:
                # typically, T.Literal here
                source_columns = []
        return source_columns

    def to_source_columns(
        self, alias_mapping: Dict[str, Union[Table, SubQuery]], metadata=TableMetadata()
    ) -> Set["Column"]:
        """
        Best guess for source table given all the possible table/subquery and their alias.
        """

        def _to_src_col(
            name: str, parent: Optional[Union[Table, SubQuery]] = None
        ) -> Column:
            col = Column(name)
            if parent:
                col.parent = parent
            return col

        source_columns: Set[Column] = set()
        alias_mapping_values = set(alias_mapping.values())
        for src_col, qualifier in self.source_columns:
            if qualifier is None:
                if src_col == "*":
                    # select *
                    for table in alias_mapping_values:
                        source_columns.add(_to_src_col(src_col, table))
                else:
                    # select unqualified column
                    src_column = _to_src_col(src_col, None)
                    if len(alias_mapping_values) == 1:
                        # in case of only one table, we get the right answer
                        src_column.parent = next(iter(alias_mapping_values))
                    else:
                        # in case of multiple tables, try to match col with schema
                        if metadata.schema_fetcher:
                            for table in alias_mapping_values:
                                if isinstance(table, Table):
                                    table_schema = metadata.get_schema(str(table))
                                    if src_col in table_schema:
                                        src_column.parent = table
                                        break
                                # TODO: support subquery

                        if len(src_column.parent_candidates) == 0:
                            # if cannot determine the table, a bunch of possible tables are set
                            for table in alias_mapping_values:
                                src_column.parent = table
                    source_columns.add(src_column)
            else:
                parent_table = alias_mapping.get(qualifier) or Table(qualifier)
                source_columns.add(_to_src_col(src_col, parent_table))
        return source_columns
