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

from typing import Iterator
from typing import Optional

from collections import OrderedDict

from perkeepy.sortedkv import KV
from perkeepy.sortedkv import SortedKV


class OrderedDictKeyValue:
    def __init__(self, key: str, value: str) -> None:
        self._key = key
        self._value = value

    def key(self) -> str:
        return self._key

    def value(self) -> str:
        return self._value

    @staticmethod
    def _assert_implements_kv(kv: "OrderedDictKeyValue") -> KV:
        return kv


class OrderedDictSortedKV:
    def __init__(self) -> None:
        self._dict: OrderedDict[str, str] = OrderedDict()

    def get(self, key: str) -> Optional[str]:
        return self._dict.get(key, None)

    def set(self, key: str, value: str) -> None:
        self._dict[key] = value
        for key in sorted(self._dict.keys()):
            self._dict.move_to_end(key)

    def delete(self, key: str) -> None:
        """Deleting non-existent keys is OK"""
        self._dict.pop(key, None)

    def find(self, start: str, end: Optional[str]) -> Iterator[KV]:
        """
        Returns an iterator starting at the first key greater or equal
        to 'start' but smaller than 'end'.
        """
        for key, value in self._dict.items():
            if key >= start and (end is None or key < end):
                yield OrderedDictKeyValue(key=key, value=value)

    @staticmethod
    def _assert_implements_sortedkv(d: "OrderedDictSortedKV") -> SortedKV:
        return d
