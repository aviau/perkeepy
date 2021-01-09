from typing import Optional

from perkeepy.blob import Ref
from perkeepy.schema import CamliType


class BlobMeta:
    def __init__(
        self, ref: Ref, size: int, schema_type: Optional[CamliType]
    ) -> None:
        self._ref = ref
        self._size = size
        self._schema_type = schema_type
