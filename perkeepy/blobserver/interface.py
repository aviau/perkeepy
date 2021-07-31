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
from typing import Protocol

from perkeepy.blob import Blob
from perkeepy.blob import Fetcher
from perkeepy.blob import Ref


class BlobEnumerator(Protocol):
    def enumerate_blobs(self, after: Optional[Ref]) -> Iterator[Ref]:
        ...


class BlobReceiver(Protocol):
    def receive_blob(self, blob: Blob) -> None:
        ...


class Storage(Fetcher, BlobEnumerator, BlobReceiver, Protocol):
    """
    Storage is the interface that must be implemented by a blobserver
    storage type. (e.g. localdisk, s3, encrypt, shard, replica, remote)
    """

    ...
