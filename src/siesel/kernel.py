# c-basic-offset: 4; tab-width: 8; indent-tabs-mode: nil
# vi: set shiftwidth=4 tabstop=8 expandtab:
# :indentSize=4:tabSize=8:noTabs=true:
#
# SPDX-FileCopyrightText: Copyright 2024-present Intel Corporation.
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Kernel repo functions
"""

import os
from sys import stderr


def validate_repo(path: str) -> int:
    """Validate is the kernel git repo"""

    if not os.path.exists(path):
        print(f"{path}: not found", file=stderr)
        return 1

    p = os.path.join(path, ".git")
    if not os.path.exists(p):
        print(f"{p}: not found. Is not a git repo", file=stderr)
        return 1

    p = os.path.join(path, "drivers", "cxl")
    if not os.path.exists(p):
        print(f"{p}: CXL source code not found", file=stderr)
        return 1

    return 0


def get_cxl_features(kernel_path: str) -> int:
    """Get the CXL features from the kernel repo"""

    if validate_repo(kernel_path):
        return 1

    return 0
