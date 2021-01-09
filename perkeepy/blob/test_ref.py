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

from perkeepy.blob import Ref
from perkeepy.blob.ref import SHA224Ref


def test_from_str_sha224() -> None:
    ref_sha224: Ref = Ref.from_ref_str(
        "sha224-d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f"
    )
    assert ref_sha224.get_digest_name() == "sha224"
    assert (
        ref_sha224.get_bytes().hex()
        == "d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f"
    )
    assert (
        ref_sha224.to_str()
        == "sha224-d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f"
    )


def test_ref_equal() -> None:
    assert Ref.from_ref_str(
        "sha224-d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f"
    ) == Ref.from_ref_str(
        "sha224-d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f"
    )
