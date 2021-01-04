from typing import Iterator
from typing import Optional

from perkeepy.blob import Ref


class S3:
    def __init__(self) -> None:
        ...

    def enumerate_blobs(self, after: Optional[Ref]) -> Iterator[Ref]:
        raise Exception()

    def fetch(self, ref: Ref) -> bytes:
        raise Exception()

    @staticmethod
    def _assert_implements_storage(s3: "S3") -> None:
        from perkeepy.blobserver import Storage

        storage: Storage = s3
