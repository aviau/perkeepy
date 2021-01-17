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

from dataclasses import dataclass

from perkeepy.blob import Blob
from perkeepy.blob import Ref


@dataclass
class HaveValue:
    indexed: bool


class KeyValueBuilder:
    """
    Builds keys and values for SortedKVIndex
    """

    def get_have_key(self, ref: Ref) -> str:
        return f"have:{ref.to_str()}"

    def get_have_value(self, blob: Blob) -> str:
        raise NotImplementedError()

    def parse_have_value(self, value: str) -> HaveValue:
        indexed: bool = value.endswith("|indexed")
        return HaveValue(indexed=indexed)
