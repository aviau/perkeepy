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
                bytes_ref_blob: Blob = self._fetcher.fetch(
                    Ref.from_ref_str(bytes_ref_str)
                )
                full_read += BytesReader(
                    blob=BytesSchema(schema=Schema.from_blob(bytes_ref_blob)),
                    fetcher=self._fetcher,
                ).read()

            elif part.get("blobRef"):
                blob_ref_str: str = part["blobRef"]
                blob_ref_blob: Blob = self._fetcher.fetch(
                    Ref.from_ref_str(blob_ref_str)
                )
                full_read += blob_ref_blob.get_bytes()

        return bytes(full_read)

    @staticmethod
    def _assert_implements_reader(br: "BytesReader") -> Reader:
        return br
