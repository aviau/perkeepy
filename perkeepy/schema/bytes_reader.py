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
from typing import Protocol
from typing import Union

from perkeepy.blob import Blob
from perkeepy.blob import Fetcher
from perkeepy.blob import Ref
from perkeepy.typing import Reader

from .schema import BytesPart
from .schema import BytesSchema
from .schema import FileSchema
from .schema import Schema


class ContainsBytesParts(Protocol):
    """
    Could be a File schema or could be a Bytes Schema, we don't care
    """

    def get_parts(self) -> List[BytesPart]:
        ...


class BytesReader:
    def __init__(
        self,
        blob: ContainsBytesParts,
        fetcher: Fetcher,
    ) -> None:
        self._blob: ContainsBytesParts = blob
        self._fetcher: Fetcher = fetcher

    def read(self, size: Optional[int] = None) -> bytes:
        if size is not None:
            raise Exception("size is not yet supported")

        full_read = bytearray()

        for part in self._blob.get_parts():

            if part.get("bytesRef"):
                bytes_ref_str: str = part["bytesRef"]
                bytes_ref_blob: Blob = self._fetcher.fetch_blob(
                    Ref.from_ref_str(bytes_ref_str)
                )
                full_read += BytesReader(
                    blob=BytesSchema(schema=Schema.from_blob(bytes_ref_blob)),
                    fetcher=self._fetcher,
                ).read()

            elif part.get("blobRef"):
                blob_ref_str: str = part["blobRef"]
                blob_ref_blob: Blob = self._fetcher.fetch_blob(
                    Ref.from_ref_str(blob_ref_str)
                )
                full_read += blob_ref_blob.get_bytes()

        return bytes(full_read)

    @staticmethod
    def _assert_implements_reader(br: "BytesReader") -> Reader:
        return br
