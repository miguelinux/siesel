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
from siesel.kernel import get_cxl_features


def main(args=None):
    """
    Siesel main funcion
    """
    myargs = parse_args(args, __name__)
    conf = get_config(myargs)

    return get_cxl_features(conf["kernel_path"])


if __name__ == "__main__":
    import sys

    sys.exit(main(sys.argv[1:]))
