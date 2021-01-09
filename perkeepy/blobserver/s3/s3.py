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
from typing import List
from typing import Optional
from typing import Protocol
from typing import TypedDict

from botocore.response import StreamingBody

from perkeepy.blob import Blob
from perkeepy.blob import Ref
from perkeepy.blobserver import Storage


class S3ObjectMetadata(TypedDict):
    Key: str


class S3ListObjectsV2Response(TypedDict):
    Contents: List[S3ObjectMetadata]


class S3GetObjectResponse(TypedDict):
    Body: StreamingBody


class S3Client(Protocol):
    def list_objects_v2(
        self,
        *,
        Bucket: str,
        Prefix: Optional[str] = None,
        StartAfter: str,
    ) -> S3ListObjectsV2Response:
        ...

    def get_object(
        self,
        *,
        Bucket: str,
        Key: str,
    ) -> S3GetObjectResponse:
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
                ref = Ref.from_ref_str(ref_str)
                yield ref

            after = ref

    def fetch_blob(self, ref: Ref) -> Blob:
        resp: S3GetObjectResponse = self.client.get_object(
            Bucket=self.bucket,
            Key=self.dirprefix + ref.to_str(),
        )
        blob: Blob = Blob(
            ref=ref,
            readall=lambda: resp["Body"].read(),
        )
        return blob

    def receive_blob(self, blob: Blob) -> None:
        raise NotImplementedError()

    @staticmethod
    def _assert_implements_storage(s3: "S3") -> Storage:
        return s3
