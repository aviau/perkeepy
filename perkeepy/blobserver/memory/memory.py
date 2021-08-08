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

from perkeepy.blob import Blob
from perkeepy.blob import Ref
from perkeepy.blobserver import Storage


class MemoryBlobServer:
    """Memory-based blob server. Mostly used for tests."""

    def __init__(
        self,
    ) -> None:
        self.blobs: dict[str, Blob] = dict()

    def enumerate_blobs(self, after: Optional[Ref] = None) -> Iterator[Ref]:
        if after:
            raise Exception("after is not yet supported")
        for _, blob in sorted(self.blobs.items(), key=lambda x: x[0]):
            yield blob.get_ref()

    def fetch_blob(self, ref: Ref) -> Optional[Blob]:
        return self.blobs.get(ref.to_str())

    def receive_blob(self, blob: Blob) -> None:
        self.blobs[blob.get_ref().to_str()] = blob

    @staticmethod
    def _assert_implements_storage(bs: "MemoryBlobServer") -> Storage:
        return bs
