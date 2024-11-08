import pandas as pd
from tlc.client.sample_type import SampleType as SampleType
from tlc.core.object_registry import ObjectTypeRegistry as ObjectTypeRegistry
from tlc.core.objects.tables.in_memory_rows_table import _InMemoryRowsTable
from tlc.core.schema import Schema as Schema
from tlc.core.url import Url as Url
from typing import Any

class TableFromPandas(_InMemoryRowsTable):
    """A table populated from a Pandas Dataframe object"""
    def __init__(self, url: Url | None = None, created: str | None = None, description: str | None = None, row_cache_url: Url | None = None, row_cache_populated: bool | None = None, override_table_rows_schema: Schema | None = None, init_parameters: Any | None = None, dataframe: pd.DataFrame | None = None, input_tables: list[Url] | None = None) -> None: ...
