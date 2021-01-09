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

from typing import Callable
from typing import Optional

from .ref import Hash
from .ref import Ref

ReadAll = Callable[[], bytes]


class Blob:
    def __init__(self, ref: Ref, readall: ReadAll) -> None:
        self._ref: Ref = ref
        self.readall: ReadAll = readall
        self._bytes: Optional[bytes] = None

    def get_ref(self) -> Ref:
        return self._ref

    def get_bytes(self) -> bytes:
        if self._bytes is None:
            self._bytes = self.readall()
        return self._bytes

    def is_utf8(self) -> bool:
        try:
            self.get_bytes().decode("utf-8")
        except UnicodeDecodeError:
            return False
        return True

    def is_valid(self) -> bool:
        hash_: Hash = self._ref.get_new_hash()
        hash_.update(self.get_bytes())
        return hash_.hexdigest() == self._ref.get_hexdigest()

    @classmethod
    def from_contents_bytes(cls, data: bytes) -> "Blob":
        ref: Ref = Ref.from_contents_bytes(data)
        return cls(ref=ref, readall=lambda: data)

    @classmethod
    def from_contents_str(cls, data: str) -> "Blob":
        return cls.from_contents_bytes(data.encode("utf-8"))
