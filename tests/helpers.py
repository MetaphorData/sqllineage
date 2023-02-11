from sqllineage.core.models import Column, Table, TableMetadata
from sqllineage.runner import LineageRunner


def assert_table_lineage_equal(
    sql,
    source_tables=None,
    target_tables=None,
    default_database=None,
    default_schema=None,
):
    lr = LineageRunner(
        sql,
        TableMetadata(default_database=default_database, default_schema=default_schema),
    )
    _assert_source_target_tables(lr, source_tables, target_tables)


def _assert_source_target_tables(
    lr: LineageRunner, source_tables=None, target_tables=None
):
    for _type, actual, expected in zip(
        ["Source", "Target"],
        [lr.source_tables, lr.target_tables],
        [source_tables, target_tables],
    ):
        actual = set(actual)
        expected = (
            set()
            if expected is None
            else {Table(t) if isinstance(t, str) else t for t in expected}
        )
        assert (
            actual == expected
        ), f"\n\tExpected {_type} Table: {expected}\n\tActual {_type} Table: {actual}"


def assert_column_lineage_equal(
    sql,
    column_lineages=None,
    default_database=None,
    default_schema=None,
    schema_fetcher=None,
    exclude_subquery=True,
):
    lr = LineageRunner(
        sql,
        TableMetadata(
            default_database=default_database,
            default_schema=default_schema,
            schema_fetcher=schema_fetcher,
        ),
    )
    _assert_column_lineage(lr, column_lineages, exclude_subquery)


def _assert_column_lineage(
    lr: LineageRunner,
    column_lineages=None,
    exclude_subquery=True,
):
    expected = set()
    for src, tgt in column_lineages or []:
        src_col = Column(src.column)
        if src.qualifier is not None:
            src_col.parent = Table(src.qualifier)
        tgt_col = Column(tgt.column)
        tgt_col.parent = Table(tgt.qualifier)
        expected.add((src_col, tgt_col))

    fetched_lineages = set(lr.get_column_lineage(exclude_subquery))
    actual = {(lineage[0], lineage[-1]) for lineage in fetched_lineages}
    assert (
        set(actual) == expected
    ), f"\n\tExpected Lineage: {expected}\n\tActual Lineage: {actual}"


def assert_table_and_column_lineage_equal(
    sql,
    source_tables=None,
    target_tables=None,
    column_lineages=None,
    schema_fetcher=None,
    default_database=None,
    default_schema=None,
    exclude_subquery=True,
):
    lr = LineageRunner(
        sql,
        TableMetadata(
            default_database=default_database,
            default_schema=default_schema,
            schema_fetcher=schema_fetcher,
        ),
    )
    lr._eval()

    _assert_source_target_tables(lr, source_tables, target_tables)

    _assert_column_lineage(lr, column_lineages, exclude_subquery)
