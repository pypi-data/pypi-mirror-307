from _typeshed import Incomplete
from pycocotools.coco import COCO
from tlc.core.builtins.constants.column_names import BOUNDING_BOXES as BOUNDING_BOXES, BOUNDING_BOX_LIST as BOUNDING_BOX_LIST, HEIGHT as HEIGHT, IMAGE as IMAGE, IMAGE_HEIGHT as IMAGE_HEIGHT, IMAGE_WIDTH as IMAGE_WIDTH, LABEL as LABEL, SEGMENTATION as SEGMENTATION, WIDTH as WIDTH, X0 as X0, X1 as X1, Y0 as Y0, Y1 as Y1
from tlc.core.builtins.constants.display_importances import DISPLAY_IMPORTANCE_BOUNDING_BOX as DISPLAY_IMPORTANCE_BOUNDING_BOX, DISPLAY_IMPORTANCE_IMAGE as DISPLAY_IMPORTANCE_IMAGE
from tlc.core.builtins.constants.number_roles import NUMBER_ROLE_BB_MIN_X as NUMBER_ROLE_BB_MIN_X, NUMBER_ROLE_BB_MIN_Y as NUMBER_ROLE_BB_MIN_Y, NUMBER_ROLE_BB_SIZE_X as NUMBER_ROLE_BB_SIZE_X, NUMBER_ROLE_BB_SIZE_Y as NUMBER_ROLE_BB_SIZE_Y
from tlc.core.builtins.constants.string_roles import STRING_ROLE_FOLDER_URL as STRING_ROLE_FOLDER_URL, STRING_ROLE_URL as STRING_ROLE_URL
from tlc.core.builtins.schemas import BoundingBoxListSchema as BoundingBoxListSchema
from tlc.core.builtins.types.bounding_box import TopLeftXYWHBoundingBox as TopLeftXYWHBoundingBox
from tlc.core.object_type_registry import ObjectTypeRegistry as ObjectTypeRegistry
from tlc.core.objects.table import TableRow as TableRow
from tlc.core.objects.tables.in_memory_rows_table import _InMemoryRowsTable
from tlc.core.schema import ImageUrlStringValue as ImageUrlStringValue, Int32Value as Int32Value, MapElement as MapElement, Schema as Schema, StringValue as StringValue
from tlc.core.url import Url as Url
from typing import Any

logger: Incomplete

class TableFromCoco(_InMemoryRowsTable):
    """A table populated from a annotations json-file and a image folder.

    References:
    COCO data format: https://cocodataset.org/#format-data
    COCO data format APIs: https://github.com/cocodataset/cocoapi
    """
    input_url: Incomplete
    image_folder_url: Incomplete
    def __init__(self, url: Url | None = None, created: str | None = None, description: str | None = None, row_cache_url: Url | None = None, row_cache_populated: bool | None = None, override_table_rows_schema: Any = None, input_url: Url | str | None = None, image_folder_url: Url | str | None = None, init_parameters: Any = None, input_tables: list[Url] | None = None) -> None: ...
    @property
    def coco(self) -> COCO:
        """Load COCO object from input_url if not already loaded."""
