from perkeepy.blob import Blob


class Schema:
    """
    A schema is a JSON-encoded blob that describes other blobs. We recognize
    a schema by the presence of the "camliVersion" and "camliType" fields.
    """

    @classmethod
    def from_blob(cls, blob: Blob) -> "Schema":
        raise NotImplementedError()
