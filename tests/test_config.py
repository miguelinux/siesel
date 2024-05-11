# c-basic-offset: 4; tab-width: 8; indent-tabs-mode: nil
# vi: set shiftwidth=4 tabstop=8 expandtab:
# :indentSize=4:tabSize=8:noTabs=true:
#
# SPDX-FileCopyrightText: Copyright 2024-present Intel Corporation.
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Prueba de config.py
"""

import os
from argparse import Namespace

import pytest

from siesel.config import read_conf_cmdline
from siesel.config import read_conf_env


@pytest.mark.parametrize(
    "kernel_path,config_file",
    [("a_path", "a_file"), ("a_path", None), (None, "a_file"), (None, None)],
)
def test_read_conf_env(kernel_path, config_file):
    """Test the read conf env function"""
    expected = {}
    if kernel_path:
        os.environ["SIESEL_KERNEL_PATH"] = kernel_path
        expected["kernel_path"] = kernel_path
    if config_file:
        os.environ["SIESEL_CONFIG_FILE"] = config_file
        expected["config_file"] = kernel_path
    assert expected == read_conf_env(expected)  # nosec B101


@pytest.mark.parametrize(
    "kernel_path,config_file",
    [("a_path", "a_file"), ("a_path", None), (None, "a_file"), (None, None)],
)
def test_read_conf_cmdline(kernel_path, config_file):
    """Test the read conf env function"""

    class _TArgs(Namespace):
        kernel_path = "test value"
        config_file = "test value"

    targs = _TArgs()
    expected = {
        "kernel_path": "test value",
        "config_file": "test value",
    }
    tconf = {
        "kernel_path": "any value",
        "config_file": "any value",
    }

    if kernel_path:
        expected["kernel_path"] = kernel_path
        targs.kernel_path = kernel_path
    if config_file:
        expected["config_file"] = config_file
        targs.config_file = config_file

    assert expected == read_conf_cmdline(targs, tconf)  # nosec B101
