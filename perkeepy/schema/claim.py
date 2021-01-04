from perkeepy.blob import Blob


class Claim:
    """
    A claim is a JSON-signed schema blob. We recognize a claim if it
    has the "camliVersion" field.
    """

    @classmethod
    def from_blob(cls, blob: Blob) -> "Claim":
        raise NotImplementedError()
