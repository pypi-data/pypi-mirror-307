"""
Linton 'publish' subcommand
© Reuben Thomas <rrt@sc3d.org> 2024
Released under the GPL version 3, or (at your option) any later version.
"""

import os
import argparse
import shutil
import subprocess

from linton.warnings import die
from linton.argparse_util import add_subcommand_arguments


def publish(args: argparse.Namespace, render_env: dict[str, str]) -> None:
    """'publish' command handler"""
    # Check output either does not exist, or is an empty directory, unless
    # --force given.
    if os.path.exists(args.output) and not (
        os.path.isdir(args.output) and len(os.listdir(args.output)) == 0
    ):
        if not args.force:
            die(f"output {args.output} is not an empty directory")
        shutil.rmtree(args.output)

    # Render the project files to the output
    subprocess.check_output(["nancy", args.document_root, args.output], env=render_env)


def add_subparser(subparsers: argparse._SubParsersAction) -> None:  # type: ignore[type-arg]
    parser = subparsers.add_parser(
        "publish",
        help="convert a directory of Markdown files and other resources into a web site.",
        epilog="The output DIRECTORY cannot be a subdirectory of the source directory.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite output directory even if it is not empty",
    )
    parser.add_argument(
        "--base-url",
        metavar="URL",
        help="base URL of web site relative to root of server [default: %(default)s]",
        default="/",
    )
    add_subcommand_arguments(parser)
    parser.add_argument("output", metavar="DIRECTORY", help="output directory")
    parser.set_defaults(func=publish)
