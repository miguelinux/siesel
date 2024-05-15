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
from sys import stderr

from siesel.__about__ import __version__


def read_conf_from(path: str, conf: dict, show_file_exist=False) -> dict:
    """Read configuration from a file located in path variable"""
    # the items are: variable and value (i.e. variable = value)
    two_items = 2
    values = {}
    if os.path.exists(path):
        with open(path, encoding="utf-8") as conf_file:
            for line in conf_file:
                if not line or not line.strip():
                    continue
                if line.strip()[0] == "#":
                    continue

                item = line.split("=")
                if len(item) == two_items:
                    values[item[0].strip().lower()] = item[1].strip().lower()

        for val in conf:
            if val in values:
                conf[val] = values[val]

    # The file in path does not exist
    elif show_file_exist:
        print(f"{path}: not found", file=stderr)

    return conf


def read_conf_env(conf: dict) -> dict:
    """Read configuration from environment variables"""
    k_p = os.environ.get("SIESEL_KERNEL_PATH")
    c_f = os.environ.get("SIESEL_CONFIG_FILE")
    f_t = os.environ.get("SIESEL_FROM_TAG")
    t_t = os.environ.get("SIESEL_TO_TAG")
    if k_p:
        conf["kernel_path"] = k_p
    if c_f:
        conf["config_file"] = c_f
    if f_t:
        conf["from_tag"] = f_t
    if t_t:
        conf["to_tag"] = t_t
    return conf


def read_conf_cmdline(args: Namespace, conf: dict) -> dict:
    """Read configuration from command line arguments"""
    if args.kernel_path != ".":
        conf["kernel_path"] = args.kernel_path
    if args.config_file:
        conf["config_file"] = args.config_file
    if args.from_tag:
        conf["from_tag"] = args.from_tag
    if args.to_tag:
        conf["to_tag"] = args.to_tag
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
        "from_tag": "",
        "to_tag": "",
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

        # Read config file provided by cmdline
        if myconf["config_file"]:
            myconf = read_conf_from(myconf["config_file"], myconf, show_file_exist=True)

    elif myos == "Darwin":
        pass
        # Do a test on Mac OS
    elif myos == "Windows":
        pass
        # Do a test on Windows OS

    return myconf


def parse_args(vargs: list, prog_name: str = __name__) -> object:
    """Parse arguments from command line interface"""
    parser = ArgumentParser(
        prog=prog_name,
        description="Script to identify CXL features from Linux Kernel.",
    )
    parser.add_argument(
        "-k",
        "--kernel",
        action="store",
        default=".",
        metavar="PATH",
        dest="kernel_path",
        help='path to the Kernel repo (default ".").',
    )
    parser.add_argument(
        "-c",
        "--config",
        action="store",
        default="",
        metavar="FILE",
        dest="config_file",
        help="specify the config file.",
    )
    parser.add_argument(
        "-f",
        "--from",
        action="store",
        default="",
        metavar="COMMIT/TAG",
        dest="from_tag",
        help="specify the commit id or tag to start to looking for features.",
    )
    parser.add_argument(
        "-t",
        "--to",
        action="store",
        default="HEAD",
        metavar="COMMIT/TAG",
        dest="to_tag",
        help="specify the latest commit id or tag to looking for features.",
    )
    parser.add_argument(
        "--version", action="version", version="%(prog)s " + __version__
    )

    return parser.parse_args(vargs)
