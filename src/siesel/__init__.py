# c-basic-offset: 4; tab-width: 8; indent-tabs-mode: nil
# vi: set shiftwidth=4 tabstop=8 expandtab:
# :indentSize=4:tabSize=8:noTabs=true:
#
# SPDX-FileCopyrightText: Copyright 2024-present Intel Corporation.
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Siesel (CXL) init module
"""

from siesel.config import get_config
from siesel.config import parse_args


def main():
    """
    Siesel main funcion
    """
    args = parse_args()
    conf = get_config(args)

    print("Hola Miguel")
    print(args.config_file)
    print(conf)

    return 0


if __name__ == "__main__":
    import sys

    sys.exit(main())
