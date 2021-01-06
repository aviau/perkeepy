from typing import Protocol
from typing import Type
from typing import runtime_checkable

import enum
import hashlib

from perkeepy.typing import assert_never


class Hash(Protocol):
    def update(self, bytes: bytes) -> None:
        ...

    def digest(self) -> bytes:
        ...

    def hexdigest(self) -> str:
        ...


class DigestAlgorithm(Protocol):
    def get_new_hash(self) -> Hash:
        ...

    def get_digest_name(self) -> str:
        ...


class Ref:
    def __init__(
        self, digest_algorithm: DigestAlgorithm, bytes_: bytes
    ) -> None:
        self._digest_algorithm = digest_algorithm
        self._bytes = bytes_

    def get_digest_algorithm(self) -> DigestAlgorithm:
        return self._digest_algorithm

    def get_new_hash(self) -> Hash:
        return self.get_digest_algorithm().get_new_hash()

    def get_bytes(self) -> bytes:
        return self._bytes

    def get_hexdigest(self) -> str:
        return self.get_bytes().hex()

    def get_digest_name(self) -> str:
        return self.get_digest_algorithm().get_digest_name()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ref):
            return False
        return (
            self.get_digest_name() == other.get_digest_name()
            and self.get_bytes() == other.get_bytes()
        )

    def to_str(self) -> str:
        digest_name: str = self.get_digest_name()
        hexdigest: str = self.get_hexdigest()
        return f"{digest_name}-{hexdigest}"

    @staticmethod
    def get_currently_recommended_digest_algorithm() -> DigestAlgorithm:
        return SHA224()

    @classmethod
    def from_ref_str(cls, ref: str) -> "Ref":
        """Creates a ref from a 'digalg-blobref' string"""
        digalg_name, hexdigest = ref.split("-")
        return cls(
            digest_algorithm=DigestAlgorithmName.get_digest_algorithm_from_name(
                digalg_name,
            ),
            bytes_=bytearray.fromhex(hexdigest),
        )

    @classmethod
    def from_contents_str(cls, data: str) -> "Ref":
        return cls.from_contents_bytes(data.encode("utf-8"))

    @classmethod
    def from_contents_bytes(cls, data: bytes) -> "Ref":
        """Returns a blobref using the currently recommended hash function"""
        digest_alg = cls.get_currently_recommended_digest_algorithm()
        hasher = digest_alg.get_new_hash()
        hasher.update(data)
        return Ref.from_ref_str(
            f"{digest_alg.get_digest_name()}-{hasher.hexdigest()}"
        )


class DigestAlgorithmName(enum.Enum):
    SHA224 = "sha224"

    @staticmethod
    def get_digest_algorithm_from_name(name: str) -> DigestAlgorithm:
        digalg: DigestAlgorithmName = DigestAlgorithmName(name)
        if digalg is DigestAlgorithmName.SHA224:
            return SHA224()
        else:
            assert_never(digalg)


class SHA224:
    @staticmethod
    def get_digest_name() -> str:
        return DigestAlgorithmName.SHA224.value

    @staticmethod
    def get_new_hash() -> Hash:
        return hashlib.sha224()

    @staticmethod
    def _assert_implements_digest_algorithm(sha224: "SHA224") -> None:
        f: DigestAlgorithm = sha224


class SHA224Ref(Ref):
    def get_digest_algorithm(self) -> DigestAlgorithm:
        return SHA224()
