# perkeepy

Python utilities for [Perkeep](https://perkeep.org/).

I have recently started hacking on Perkeep and implementing some of the internals in Python helps me validate my understanding of the codebase. Having a second implementation also allows for validating the formats and protocols. The intended purpose is at least to be able to browse a Perkeep storage and fetch files without the Go implementation. The API is similar to the Go implementation's.

## Things you can already do with perkeepy

```python
import boto3

from perkeepy.blob import Ref
from perkeepy.blob import Blob
from perkeepy.blobserver.s3 import S3

# Browse a blobserver on S3
s3_client: S3Client = boto3.client("s3")
blobserver = S3(s3_client=s3_client, bucket="bucket")

# Fetch Specific blobs
blob = blobserver.fetch(
    Ref.from_ref_str("sha224-ff70c8d9921031e339f792c855dd62e7fc53565828387b1f76e87c2b")
)

# Enumerate all blobs
blobs = blobserver.enumerate_blobs()
```
