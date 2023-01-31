from typing import Dict, List, Optional


class SchemaFetcher:
    """
    This class provides capability to fetch the schema (columns) of a given table
    """

    def get_schema(
        self, table: str, platform: Optional[str] = None, account: Optional[str] = None
    ) -> List[str]:
        """
        get the column names of the table
        """
        raise NotImplementedError


class DummySchemaFetcher(SchemaFetcher):
    """
    Dummy schema fetch that uses pre-defined schemas
    """

    def __init__(self, tableSchemas: Dict[str, List[str]]) -> None:
        self._schemas = tableSchemas

    def get_schema(
        self, table: str, platform: Optional[str] = None, account: Optional[str] = None
    ) -> List[str]:
        return self._schemas.get(table, [])
