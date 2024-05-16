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

from git import Repo


def get_kernel_version(path: str) -> dict:
    """Get the current kernel version from Makefile"""

    kernel_version = {
        "version": "0",
        "patchlevel": "0",
        "sublevel": "0",
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


def get_previous_release_kernel_version(current_kernel: dict) -> dict:
    """Get the previos kernel release which is NOT a -RC version"""

    previous_kernel = current_kernel.copy()

    if previous_kernel["extraversion"]:
        previous_kernel["extraversion"] = ""

    if previous_kernel["sublevel"] != "0":
        previous_kernel["sublevel"] = "0"

    if previous_kernel["patchlevel"] == "0":
        # Currently this is guessing, we need to set properly
        previous_kernel["patchlevel"] = "19"
        previous_kernel["version"] = str(int(previous_kernel["version"]) - 1)
    else:
        previous_kernel["patchlevel"] = str(int(previous_kernel["patchlevel"]) - 1)

    return previous_kernel


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
    repo = Repo(conf["kernel_path"])

    cxl_path = os.path.join(conf["kernel_path"], "drivers", "cxl")

    if not conf["from_tag"]:
        previous = get_previous_release_kernel_version(kernel_version)
        revision = "v" + previous["version"] + "." + previous["patchlevel"]
    else:
        revision = conf["from_tag"]

    revision += "..." + conf["to_tag"]

    commits_gen = repo.iter_commits(rev=revision, paths=cxl_path)
    # commits = list(commits_gen)
    for c in commits_gen:
        if "fix" in c.summary.lower() or "Merge" in c.summary:
            continue
        print(c.summary)
        # print(c.message)

    return 0
