# Copyright 2021 The Perkeepy Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
