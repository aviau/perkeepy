from typing import Iterator
from typing import List
from typing import Optional
from typing import Protocol
from typing import TypedDict

from perkeepy.blob import Ref


class S3ObjectMetadata(TypedDict):
    Key: str


class S3ListObjectsV2Response(TypedDict):
    Contents: List[S3ObjectMetadata]


class S3Client(Protocol):
    def list_objects_v2(
        self,
        *,
        Bucket: str,
        Prefix: Optional[str] = None,
        StartAfter: str,
    ) -> S3ListObjectsV2Response:
        ...


class S3:
    def __init__(
        self,
        *,
        s3_client: S3Client,
        bucket: str,
        dirprefix: Optional[str] = None,
    ) -> None:
        self.client: S3Client = s3_client
        self.bucket: str = bucket
        self.dirprefix: str = dirprefix.strip("/") + "/" if dirprefix else ""

    def enumerate_blobs(self, after: Optional[Ref] = None) -> Iterator[Ref]:
        while True:
            after_str: str = self.dirprefix + after.to_str() if after else ""

            resp: S3ListObjectsV2Response = self.client.list_objects_v2(
                Bucket=self.bucket,
                Prefix=self.dirprefix,
                StartAfter=after_str,
            )

            if not resp.get("Contents"):
                break

            for s3_object in resp["Contents"]:
                ref_str: str = s3_object["Key"].split("/")[-1]
                ref = Ref.from_str(ref_str)
                yield ref

            after = ref

    def fetch(self, ref: Ref) -> bytes:
        raise NotImplementedError()

    @staticmethod
    def _assert_implements_storage(s3: "S3") -> None:
        from perkeepy.blobserver import Storage

        storage: Storage = s3
