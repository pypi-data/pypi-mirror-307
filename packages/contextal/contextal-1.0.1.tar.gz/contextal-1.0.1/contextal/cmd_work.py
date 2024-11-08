"""
The "work" subcommand processor
"""

import argparse

from contextal.config import Config
from contextal.misc import add_profile_switch, add_pretty_switch, json_print
from contextal.platform import Platform

ARG_CMD = "work"


def add_argparser(parser):
    """Subparser"""
    subparser = parser.add_parser(
        ARG_CMD, help="work submission and related actions"
    ).add_subparsers(dest="action", help="available actions:", required=True)
    # Submit
    c = subparser.add_parser("submit", help="submit an object for processing")
    c.add_argument("file", help="file to submit", type=argparse.FileType("rb"))
    c.add_argument(
        "--ttl",
        help="number of seconds allowed to fully complete this work request (optional)",
        type=int,
    )
    c.add_argument(
        "--max-recursion",
        help="depth limit for processing nested objects",
        type=int,
    )
    c.add_argument("--org", help="organization identifier")
    add_profile_switch(c)
    # Get graph
    c = subparser.add_parser("graph", help="return the work tree in JSON form")
    c.add_argument("work_id", help="the requested work ID")
    add_pretty_switch(c)
    add_profile_switch(c)
    # Get actions
    c = subparser.add_parser(
        "actions", help="return the triggered scenario actions for a work"
    )
    c.add_argument("work_id", help="the requested work ID")
    add_pretty_switch(c)
    add_profile_switch(c)


def execute(args):
    """Executor"""
    config = Config()
    config.load_profile(args.profile)
    platform = Platform(config)
    if args.action == "submit":
        res = platform.submit_work(
            args.file,
            args.file.name,
            args.ttl,
            args.max_recursion,
            args.org,
        )
        print(res["work_id"])
    elif args.action == "graph":
        json_print(platform.get_graphs([args.work_id]), args.pretty)
    elif args.action == "actions":
        json_print(platform.get_actions(args.work_id), args.pretty)
