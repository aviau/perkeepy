#!/usr/bin/env python3
#
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

from typing import Pattern

import os
import re
import sys
from datetime import datetime

import click


@click.command()
@click.option("--check", type=bool, default=False, is_flag=True)
@click.argument("filenames", type=click.Path(exists=True), nargs=-1)
def main(*, filenames: str, check: bool) -> None:
    copyright_checker = CopyrightChecker()

    for filename in filenames:

        if copyright_checker.has_copyright(filename):
            continue

        if check:
            click.echo(f"Missing copyright on {filename}")
            sys.exit(1)

        add_header(filename)


class CopyrightChecker:
    def __init__(self) -> None:
        self._pattern = re.compile(".*Copyright [0-9]{4}")

    def has_copyright(self, filename: str) -> bool:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if self._pattern.match(line):
                    return True
        return False


def add_header(filename: str) -> None:
    _, extension = os.path.splitext(filename)

    header: str = HEADER.replace("YYYY", f"{datetime.now().year}")

    if extension == ".py":
        header = "\n# ".join(header.splitlines()).strip()
    else:
        raise Exception(f"Unsupported extension {extension}")

    # Remove trailing whitespaces
    header = "\n".join(l.strip() for l in header.splitlines())

    with open(filename, "r", encoding="utf-8") as f:
        file_before: str = f.read()

    file_after: str = header + "\n\n" + file_before

    with open(filename, "w", encoding="utf-8") as f:
        f.write(file_after)


HEADER = """
Copyright YYYY The Perkeep Authors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License
"""

if __name__ == "__main__":
    main()
