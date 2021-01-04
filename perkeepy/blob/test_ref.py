from perkeepy.blob import Ref
from perkeepy.blob.ref import SHA224Ref


def test_from_str_sha224() -> None:
    ref_sha224: Ref = Ref.from_str(
        "sha224-d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f"
    )
    assert isinstance(ref_sha224, SHA224Ref)
    assert ref_sha224.get_digest_name() == "sha224"
    assert (
        ref_sha224.get_bytes().hex()
        == "d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f"
    )


def test_ref_equal() -> None:
    assert Ref.from_str(
        "sha224-d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f"
    ) == Ref.from_str(
        "sha224-d14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f"
    )
