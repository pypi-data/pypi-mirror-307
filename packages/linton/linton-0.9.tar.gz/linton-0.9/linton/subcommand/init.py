"""
Linton 'init' subcommand
© Reuben Thomas <rrt@sc3d.org> 2024
Released under the GPL version 3, or (at your option) any later version.
"""

import os
import argparse
import importlib
import shutil

from linton.warnings import die


def init(args: argparse.Namespace) -> None:
    """'init' command handler"""
    # Check directory does not exist.
    if os.path.exists(args.directory):
        die(f"output {args.directory} already exists")

    # Copy the demo files to the new project
    with importlib.resources.as_file(importlib.resources.files()) as fspath:
        shutil.copytree(os.path.join(fspath, "init-pages"), args.directory)


def add_subparser(subparsers: argparse._SubParsersAction) -> None:  # type: ignore[type-arg]
    parser = subparsers.add_parser(
        "init",
        help="create a new Linton project",
    )
    parser.add_argument("directory", metavar="DIRECTORY", help="output directory")
    parser.set_defaults(func=init)
