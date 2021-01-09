from typing import Iterator
from typing import Optional
from typing import Protocol

from perkeepy.blob import Blob
from perkeepy.blob import Fetcher
from perkeepy.blob import Ref
from perkeepy.typing import Reader


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
