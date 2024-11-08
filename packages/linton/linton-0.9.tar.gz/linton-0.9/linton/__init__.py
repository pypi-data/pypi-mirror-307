#!/usr/bin/env python3
#
# © Reuben Thomas <rrt@sc3d.org> 2023-2024
# Released under the GPL version 3, or (at your option) any later version.

import importlib.metadata
import os
import sys
import shutil
from pathlib import Path
import argparse
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib
import warnings
from warnings import warn
from typing import (
    Optional,
    List,
    Union,
    Type,
    NoReturn,
    TextIO,
)

from xdg import Mime

from .warnings import simple_warning, die
from .subcommand.publish import publish, add_subparser as add_publish_subparser
from .subcommand.serve import serve, add_subparser as add_serve_subparser
from .subcommand.init import init, add_subparser as add_init_subparser


VERSION = importlib.metadata.version("linton")


def main(argv: List[str] = sys.argv[1:]) -> None:
    # Command-line arguments
    parser = argparse.ArgumentParser(
        description="Make a web site from Markdown files and other resources.",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {VERSION} (22 Oct 2024) by Reuben Thomas <rrt@sc3d.org>",
    )
    warnings.showwarning = simple_warning(parser.prog)

    subparsers = parser.add_subparsers(required=True, title="subcommands")
    add_publish_subparser(subparsers)
    add_serve_subparser(subparsers)
    add_init_subparser(subparsers)

    args = parser.parse_args(argv)
    if "base_url" not in args:
        args.base_url = "/"

    # Set up environment for executable $include scripts.
    render_env = dict(os.environ)
    render_env["LINTON_BASE_URL"] = args.base_url
    render_env["LINTON_DOCUMENT_ROOT"] = args.document_root

    args.func(args, render_env)
