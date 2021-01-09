from typing import Protocol

from perkeepy.blobserver import BlobReceiver

from .blob_meta import BlobMeta


class Indexer(BlobReceiver, Protocol):
    def get_blob_meta(self) -> BlobMeta:
        ...
