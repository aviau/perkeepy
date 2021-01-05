import hashlib

from perkeepy.blob import Blob
from perkeepy.blob import Ref


def test_is_utf8() -> None:
    blob: Blob = Blob(
        ref=Ref.from_ref_str(
            "sha224-d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f"
        ),
        readall=lambda: "test".encode("utf-8"),
    )
    assert blob.is_utf8()

    blob = Blob(
        ref=Ref.from_ref_str(
            "sha224-d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f"
        ),
        readall=lambda: b"\xdc",
    )
    assert not blob.is_utf8()


def test_is_valid_fail() -> None:
    blob: Blob = Blob(
        ref=Ref.from_ref_str(
            "sha224-d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f"
        ),
        readall=lambda: "test".encode("utf-8"),
    )
    assert not blob.is_valid()


def test_is_valid() -> None:
    blob_content: bytes = "test".encode("utf-8")
    hexdigest: str = hashlib.sha224(blob_content).hexdigest()
    ref: Ref = Ref.from_ref_str(f"sha224-{hexdigest}")
    blob: Blob = Blob(
        ref=ref,
        readall=lambda: blob_content,
    )
    assert blob.is_valid()


def test_from_contents_str() -> None:
    blob: Blob = Blob.from_contents_str("test")
    assert blob.get_ref().get_digest_algorithm().get_digest_name() == "sha224"
    assert (
        blob.get_ref().to_str()
        == "sha224-90a3ed9e32b2aaf4c61c410eb925426119e1a9dc53d4286ade99a809"
    )
    assert (
        blob.get_ref().get_hexdigest()
        == "90a3ed9e32b2aaf4c61c410eb925426119e1a9dc53d4286ade99a809"
    )
    assert blob.get_bytes().decode("utf-8") == "test"
    assert blob.is_valid()
