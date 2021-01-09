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

from typing import List
from typing import Optional
from typing import Tuple

from perkeepy.sortedkv import SortedKV


def run_sortedkv_test(kv: SortedKV) -> None:
    """Suite of tests to validate a SortedKV implementation"""

    # At first it should be empty
    assert is_empty(kv)

    # Add something, it shouldn't be empty anymore
    kv.set("foo", "bar")
    assert not is_empty(kv)

    # Retrieve the key
    assert kv.get("foo") == "bar"

    # Retrieve something that does not exist
    assert kv.get("bar") is None

    # Delete delete our key twice
    kv.delete("foo")
    kv.delete("foo")

    # Test the find implementation
    kv.set("a", "av")
    kv.set("c", "cv")
    kv.set("b", "bv")
    assert_find_returns(kv, "", None, [("a", "av"), ("b", "bv"), ("c", "cv")])
    assert_find_returns(kv, "a", None, [("a", "av"), ("b", "bv"), ("c", "cv")])
    assert_find_returns(kv, "b", None, [("b", "bv"), ("c", "cv")])
    assert_find_returns(kv, "a", "c", [("a", "av"), ("b", "bv")])
    assert_find_returns(kv, "a", "b", [("a", "av")])
    assert_find_returns(kv, "a", "a", [])
    assert_find_returns(kv, "d", None, [])
    assert_find_returns(kv, "d", "e", [])

    # Verify that the value isn't being used instead of the key in the range comparison.
    kv.set("y", "x:foo")
    assert_find_returns(kv, "x:", "x~", [])


def is_empty(kv: SortedKV) -> bool:
    return len(list(kv.find("", None))) == 0


def assert_find_returns(
    kv: SortedKV,
    start: str,
    end: Optional[str],
    expected_results: List[Tuple[str, str]],
) -> None:
    results: List[Tuple[str, str]] = [
        (kv.key(), kv.value()) for kv in kv.find(start, end)
    ]
    assert results == expected_results
