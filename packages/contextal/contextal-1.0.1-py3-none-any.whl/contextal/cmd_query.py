"""
The "query" subcommand processor
"""

import os
import subprocess
import sys
import tempfile

from contextal.config import Config
from contextal.misc import add_profile_switch, add_pretty_switch, json_print
from contextal.platform import Platform

ARG_CMD = "query"


def add_argparser(parser):
    """Subparser"""
    subparser = parser.add_parser(ARG_CMD, help="query platform data")
    subparser.add_argument(
        "--query",
        help="query input: either filename, '-' for stdin or omit to open EDITOR",
    )
    subparser.add_argument(
        "--objects", help="return objects rather than works", action="store_true"
    )
    alt = subparser.add_mutually_exclusive_group()
    alt.add_argument("--count", help="only count matching items", action="store_true")
    alt.add_argument("--max-items", help="return at most these items", type=int)
    add_pretty_switch(subparser)
    add_profile_switch(subparser)


def execute(args):
    """Executor"""
    config = Config()
    config.load_profile(args.profile)
    platform = Platform(config)
    closeme = None
    deleteme = None
    try:
        if not args.query:
            # Interactive mode
            editor = os.environ.get("EDITOR")
            if not editor:
                raise Exception("Interactive mode requested but $EDITOR is unset")
            fd, deleteme = tempfile.mkstemp()
            os.close(fd)
            subprocess.run([editor, deleteme], shell=False, check=True)
            # Note: Apple macOS violates POSIX in that writes are not visible by
            # subsequent reads, hence the reopening by name and the messy code
            qf = open(deleteme, "r", encoding="utf-8")
            closeme = qf
        elif args.query == "-":
            # Stdin mode
            qf = sys.stdin
        else:
            # File mode
            qf = open(args.query, "r", encoding="utf-8")
            closeme = qf
        query = qf.read()
    finally:
        if closeme:
            closeme.close()
        if deleteme:
            os.unlink(deleteme)
    if args.count:
        res = platform.count(query, args.objects)["count"]
    else:
        res = platform.search(query, args.objects, args.max_items)
    json_print(res, args.pretty)
