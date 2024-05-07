# c-basic-offset: 4; tab-width: 8; indent-tabs-mode: nil
# vi: set shiftwidth=4 tabstop=8 expandtab:
# :indentSize=4:tabSize=8:noTabs=true:
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Prueba de config.py
"""

from siesel.config import read_conf_env
import os
import pytest

@pytest.mark.parametrize("kernel_path,config_file",
                         [("a_path", "a_file"),
                          ("a_path", None),
                          (None, "a_file"),
                          (None, None)])
def test_read_conf_env(kernel_path, config_file):
    """ Test the read conf env function """
    os.environ["SIESEL_KERNEL_PATH"] = kernel_path
    os.environ["SIESEL_CONFIG_FILE"] = config_file
    expected = {"kernel_path": kernel_path,
                "config_file": config_file}
    assert expected == read_conf_env(expected)
