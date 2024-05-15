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


def get_kernel_version(path: str) -> dict:
    """Get the current kernel version from Makefile"""

    kernel_version = {
        "version": 0,
        "patchlevel": 0,
        "sublevel": 0,
        "extraversion": "",
    }

    makefile_path = os.path.join(path, "Makefile")
    # 4 values to count in Makefile
    values_count = 0
    # the items are: variable and value (i.e. variable = value)
    two_items = 2
    with open(makefile_path, encoding="utf-8") as makefile:
        # Read the Makefile
        for a_line in makefile:
            if not a_line or not a_line.strip():
                continue

            if a_line.strip()[0] == "#":
                continue

            item = a_line.split("=")
            if len(item) == two_items:
                if item[0].strip().lower() == "version":
                    kernel_version["version"] = item[1].strip()
                    values_count += 1
                if item[0].strip().lower() == "patchlevel":
                    kernel_version["patchlevel"] = item[1].strip()
                    values_count += 1
                if item[0].strip().lower() == "sublevel":
                    kernel_version["sublevel"] = item[1].strip()
                    values_count += 1
                if item[0].strip().lower() == "extraversion":
                    kernel_version["extraversion"] = item[1].strip()
                    values_count += 1

            if values_count == 4:
                break

    return kernel_version


def is_valid_git_repo(path: str) -> bool:
    """Validate is the kernel git repo"""

    if not os.path.exists(path):
        print(f"{path}: not found", file=stderr)
        return False

    p = os.path.join(path, ".git")
    if not os.path.exists(p):
        print(f"{p}: not found. Is not a git repo", file=stderr)
        return False

    p = os.path.join(path, "Makefile")
    if not os.path.exists(p):
        print(f"{p}: not found.", file=stderr)
        return False

    p = os.path.join(path, "drivers", "cxl")
    if not os.path.exists(p):
        print(f"{p}: CXL source code not found", file=stderr)
        return False

    return True


def get_cxl_features(conf: dict) -> int:
    """Get the CXL features from the kernel repo"""

    if not is_valid_git_repo(conf["kernel_path"]):
        return 1

    kernel_version = get_kernel_version(conf["kernel_path"])

    return 0
