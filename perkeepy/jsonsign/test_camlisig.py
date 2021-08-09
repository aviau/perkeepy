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

from .camlisig import CamliSig


def test_camlisig() -> None:
    armored_signature: str = """
-----BEGIN PGP SIGNATURE-----
Version: GnuPG v1.4.11 (GNU/Linux)

iQEcBAABAgAGBQJO3/DNAAoJECkxpnwm9avaf6EH/3HVJC+6ybOJDTJIInQBum9Y
FzC1I8b6xNLN0yFdDtypZUotvW9pvU2pVpbfNSmcW/OL02eR2kgL55dHxbUjbN9C
vXlvSb2QAy8IQMdA3721pMR41rNNn08w5bbAWgW/suiyN5z0pIKn3vPEHbguGeNQ
BStgOSq1WkgCozNBxPA7V5mcUx2rUOsWHYSmEY8foPdeDYcrw2pvxPN8kXk6zBrZ
ilrtaY+Yx5zPLkq8trhHPgCdf4chL+Y2kmxXMKYjU+bkmJaNycUURdncZakTEv9Y
fbBp04kbHIaN6DttEoXuU96nTyuCFhIftmV+GPbvGpl3e2yhmae5hUUt1g0o8FE=
=aSCK
-----END PGP SIGNATURE-----
"""
    expected_camlisig: str = "iQEcBAABAgAGBQJO3/DNAAoJECkxpnwm9avaf6EH/3HVJC+6ybOJDTJIInQBum9YFzC1I8b6xNLN0yFdDtypZUotvW9pvU2pVpbfNSmcW/OL02eR2kgL55dHxbUjbN9CvXlvSb2QAy8IQMdA3721pMR41rNNn08w5bbAWgW/suiyN5z0pIKn3vPEHbguGeNQBStgOSq1WkgCozNBxPA7V5mcUx2rUOsWHYSmEY8foPdeDYcrw2pvxPN8kXk6zBrZilrtaY+Yx5zPLkq8trhHPgCdf4chL+Y2kmxXMKYjU+bkmJaNycUURdncZakTEv9YfbBp04kbHIaN6DttEoXuU96nTyuCFhIftmV+GPbvGpl3e2yhmae5hUUt1g0o8FE==aSCK"
    expected_restored: str = """-----BEGIN PGP SIGNATURE-----

iQEcBAABAgAGBQJO3/DNAAoJECkxpnwm9avaf6EH/3HVJC+6ybOJDTJIInQBum9Y
FzC1I8b6xNLN0yFdDtypZUotvW9pvU2pVpbfNSmcW/OL02eR2kgL55dHxbUjbN9C
vXlvSb2QAy8IQMdA3721pMR41rNNn08w5bbAWgW/suiyN5z0pIKn3vPEHbguGeNQ
BStgOSq1WkgCozNBxPA7V5mcUx2rUOsWHYSmEY8foPdeDYcrw2pvxPN8kXk6zBrZ
ilrtaY+Yx5zPLkq8trhHPgCdf4chL+Y2kmxXMKYjU+bkmJaNycUURdncZakTEv9Y
fbBp04kbHIaN6DttEoXuU96nTyuCFhIftmV+GPbvGpl3e2yhmae5hUUt1g0o8FE=
=aSCK
-----END PGP SIGNATURE-----
"""

    assert (
        CamliSig.from_armored_gpg_signature(armored_signature)
        == expected_camlisig
    )

    assert (
        CamliSig.to_armored_gpg_signature(expected_camlisig)
        == expected_restored
    )
