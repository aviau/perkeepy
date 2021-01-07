from typing import Optional

from perkeepy.blob import Blob
from perkeepy.blob import Fetcher
from perkeepy.blob import Ref

from .schema import BytesSchema
from .schema import Schema


class BytesReader:
    def __init__(self, blob: BytesSchema, fetcher: Fetcher) -> None:
        self._blob: BytesSchema = blob
        self._fetcher: Fetcher = fetcher

    def read(self, size: Optional[int] = None) -> bytes:
        if size is not None:
            raise Exception("size is not yet supported")

        full_read = bytearray()

        for part in self._blob.get_parts():

            if part.get("bytesRef"):
                raise NotImplementedError()
            elif part.get("blobRef"):
                blob_ref_str: str = part["blobRef"]
                blob: Blob = self._fetcher.fetch(Ref.from_ref_str(blob_ref_str))
                full_read += blob.get_bytes()

        return bytes(full_read)
