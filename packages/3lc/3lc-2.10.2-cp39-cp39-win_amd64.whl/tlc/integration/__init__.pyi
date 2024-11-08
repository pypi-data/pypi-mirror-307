from .detectron2 import DetectronMetricsCollectionHook as DetectronMetricsCollectionHook, MetricsCollectionHook as MetricsCollectionHook, UMAPReduceEmbeddingsHook as UMAPReduceEmbeddingsHook, register_coco_instances as register_coco_instances
from .hugging_face import TLCTrainer as TLCTrainer
from .pytorch_lightning import lightning_module as lightning_module
from _typeshed import Incomplete

logger: Incomplete
