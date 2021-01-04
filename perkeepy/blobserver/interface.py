from typing import Iterator
from typing import Optional
from typing import Protocol

from perkeepy.blob import Fetcher
from perkeepy.blob import Ref


class BlobEnumerator(Protocol):
    def enumerate_blobs(self, after: Optional[Ref]) -> Iterator[Ref]:
        ...


class Storage(Protocol, Fetcher, BlobEnumerator):
    ...
