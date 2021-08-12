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

from perkeepy.index import Indexer
from perkeepy.index import test_index
from perkeepy.index.sortedkv import SortedKVIndex
from perkeepy.sortedkv.ordered_dict import OrderedDictSortedKV


def test_sortedkv() -> None:
    def indexer_factory() -> Indexer:
        sorted_kv_indexer: Indexer = SortedKVIndex(
            sorted_kv=OrderedDictSortedKV(),
        )
        return sorted_kv_indexer

    test_index.run_index_test(indexer_factory=indexer_factory)
