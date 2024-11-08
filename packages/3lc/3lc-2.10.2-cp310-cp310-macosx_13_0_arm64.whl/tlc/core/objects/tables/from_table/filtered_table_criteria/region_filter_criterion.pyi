from _typeshed import Incomplete
from tlc.core.builtins.constants.number_roles import NUMBER_ROLE_VERTEX_COUNT as NUMBER_ROLE_VERTEX_COUNT, NUMBER_ROLE_XY_COMPONENT as NUMBER_ROLE_XY_COMPONENT
from tlc.core.objects.tables.from_table.filtered_table_criteria.filter_criterion import ColumnFilterCriterion as ColumnFilterCriterion, FilterCriterion as FilterCriterion
from tlc.core.schema import DimensionNumericValue as DimensionNumericValue, Float64Value as Float64Value, MapElement as MapElement, Schema as Schema
from typing import Any, Mapping
from typing_extensions import Annotated

class Region2DFilterCriterion(ColumnFilterCriterion):
    region_polygon: Incomplete
    def __init__(self, attribute: str | None = None, region_polygon: list[Annotated[list[float], 2]] | None = None, init_parameters: Any = None) -> None: ...
    @staticmethod
    def from_any(any_filter_criterion: FilterCriterion | Mapping) -> Region2DFilterCriterion: ...

class Region3DFilterCriterion(Region2DFilterCriterion):
    projection_matrix: Incomplete
    projection_origo: Incomplete
    normalization_range: Incomplete
    def __init__(self, attribute: str | None = None, region_polygon: list[Annotated[list[float], 2]] | None = None, projection_matrix: Annotated[list[Annotated[list[float], 3]], 3] | None = None, projection_origo: Annotated[list[float], 3] | None = None, normalization_range: Annotated[list[Annotated[list[float], 2]], 3] | None = None, init_parameters: Any = None) -> None: ...
    @staticmethod
    def from_any(any_filter_criterion: FilterCriterion | Mapping) -> Region3DFilterCriterion: ...
