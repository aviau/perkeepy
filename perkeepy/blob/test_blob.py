import hashlib

from perkeepy.blob import Blob
from perkeepy.blob import Ref


def test_is_utf8() -> None:
    blob: Blob = Blob(
        ref=Ref.from_str(
            "sha224-d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f"
        ),
        readall=lambda: "test".encode("utf-8"),
    )
    assert blob.is_utf8()

    blob = Blob(
        ref=Ref.from_str(
            "sha224-d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f"
        ),
        readall=lambda: b"\xdc",
    )
    assert not blob.is_utf8()


def test_not_is_valid() -> None:
    blob: Blob = Blob(
        ref=Ref.from_str(
            "sha224-d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f"
        ),
        readall=lambda: "test".encode("utf-8"),
    )
    assert not blob.is_valid()


def test_is_valid() -> None:
    blob_content: bytes = "test".encode("utf-8")
    hexdigest: str = hashlib.sha224(blob_content).hexdigest()
    ref: Ref = Ref.from_str(f"sha224-{hexdigest}")
    blob: Blob = Blob(
        ref=ref,
        readall=lambda: blob_content,
    )
    assert blob.is_valid()
