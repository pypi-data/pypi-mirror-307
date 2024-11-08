"""
contextal command main
"""

import argparse
import logging

from contextal import __version__, cmd_config, cmd_work, cmd_query, cmd_scenario, cmd_download


def main():
    """contextal command main function"""
    parser = argparse.ArgumentParser(
        description="Contextal Platform command line tools"
    )
    subparser = parser.add_subparsers(dest="subcommand", required=True, help="commands")
    cmd_config.add_argparser(subparser)
    cmd_work.add_argparser(subparser)
    cmd_query.add_argparser(subparser)
    cmd_scenario.add_argparser(subparser)
    cmd_download.add_argparser(subparser)

    parser.add_argument("--debug", help="enable debug output", action="store_true")
    parser.add_argument("--version", action="version", version=__version__)
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    if args.subcommand == cmd_config.ARG_CMD:
        cmd_config.execute(args)
    elif args.subcommand == cmd_work.ARG_CMD:
        cmd_work.execute(args)
    elif args.subcommand == cmd_query.ARG_CMD:
        cmd_query.execute(args)
    elif args.subcommand == cmd_scenario.ARG_CMD:
        cmd_scenario.execute(args)
    elif args.subcommand == cmd_download.ARG_CMD:
        cmd_download.execute(args)
    return 0
