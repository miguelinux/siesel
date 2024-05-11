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
from argparse import Namespace
from platform import system

from siesel.__about__ import __version__


def read_conf_from(path: str, conf: dict) -> dict:
    """Read configuration from a file located in path variable"""
    two_items = 2
    values = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as my_file:
            for line in my_file:
                if not line:
                    continue
                if line.strip()[0] == "#":
                    continue

                item = line.split("=")
                if len(item) == two_items:
                    values[item[0].strip().lower()] = item[1].strip().lower()

        for val in conf:
            if val in values:
                conf[val] = values[val]

    return conf


def read_conf_env(conf: dict) -> dict:
    """Read configuration from environment variables"""
    kp = os.environ.get("SIESEL_KERNEL_PATH")
    cf = os.environ.get("SIESEL_CONFIG_FILE")
    if kp:
        conf["kernel_path"] = kp
    if cf:
        conf["config_file"] = cf
    return conf


def read_conf_cmdline(args: Namespace, conf: dict) -> dict:
    """Read configuration from command line arguments"""
    if args.kernel_path:
        conf["kernel_path"] = args.kernel_path
    if args.config_file:
        conf["config_file"] = args.config_file
    return conf


def get_config(args: Namespace) -> dict:
    """
    Get configuration finding/reading it, in the next order
    1. system-wide: /etc/siesel.conf
    2. $XDG_CONFIG_HOME:  $HOME/.config
    3. virtual environemnt SIESEL_XXXX
    4. command line
    """
    myos = system()
    myconf = {
        "kernel_path": ".",
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
        # Read from cmdline
        myconf = read_conf_cmdline(args, myconf)
    elif myos == "Darwin":
        pass
    elif myos == "Windows":
        pass

    return myconf


def parse_args(vargs: list) -> object:
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

    return parser.parse_args(vargs)
