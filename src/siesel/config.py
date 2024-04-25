# c-basic-offset: 4; tab-width: 8; indent-tabs-mode: nil
# vi: set shiftwidth=4 tabstop=8 expandtab:
# :indentSize=4:tabSize=8:noTabs=true:
#
# SPDX-FileCopyrightText: Copyright 2024-present Intel Corporation.
#
# SPDX-License-Identifier: GPL-3.0-or-later
"""
Config functions
"""

import os
from argparse import ArgumentParser
from platform import system

from .__about__ import __version__


def read_conf_from(path, conf):
    """Read configuration from a file located in path variable"""
    if os.path.exists():
        pass
    return None


def read_conf_env(_conf):
    """Read configuration from environment variables"""
    kp = os.environ.get("SIESEL_KERNEL_PATH")
    cf = os.environ.get("SIESEL_CONFIG_FILE")
    return None


def get_config(args):
    """
    Get configuration finding/reading it, in the next order
    1. system-wide: /etc/siesel.conf
    2. $XDG_CONFIG_HOME:  $HOME/.config
    3. virtual environemnt SIESEL_XXXX
    4. command line
    """
    myos = system()
    myconf = {
        "kernel_path": "",
        "config_file": "",
    }

    if myos == "Linux":
        # Read from system-wide
        myconf = read_conf_from("/etc/siesel.conf", myconf)
        # Read from $HOME
        home = os.environ.get("HOME")
        if home:
            myconf = read_conf_from(f"{home}/.config/siesel.conf", myconf)
        # Read from environment variables
        myconf = read_conf_env(myconf)
    elif myos == "Darwin":
        pass
    elif myos == "Windows":
        pass

    return myconf


def parse_args():
    """Parse arguments from command line interface"""
    parser = ArgumentParser(
        prog=__name__,
        description="Script to identify CXL features from Linux Kernel",
    )
    parser.add_argument(
        "-k",
        "--kernel",
        action="store",
        default=".",
        metavar="PATH",
        dest="kernel_path",
        help='path to the Kernel repo (default ".")',
    )
    parser.add_argument(
        "-c",
        "--config",
        action="store",
        default="",
        metavar="FILE",
        dest="config_file",
        help="specify the config file",
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s " + __version__
    )

    args = parser.parse_args()

    return args
