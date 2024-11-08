"""
The "scenario" subcommand processor
"""

import json
import sys

from contextal.config import Config
from contextal.misc import add_profile_switch, add_pretty_switch, json_print
from contextal.platform import Platform

ARG_CMD = "scenario"


def add_argparser(parser):
    """Subparser"""
    subparser = parser.add_parser(ARG_CMD, help="scenarios management").add_subparsers(
        dest="action", help="available actions:", required=True
    )
    # Add
    c = subparser.add_parser(
        "add", help="add a new scenario (possibly replacing an existing one)"
    )
    c.add_argument(
        "scenario_json", help="scenario in JSON form to submit (use '-' for stdin)"
    )
    c.add_argument(
        "--replace-id",
        help="the ID of the scenario to replace with the new one",
        type=int,
    )
    add_pretty_switch(c)
    add_profile_switch(c)
    # Delete
    c = subparser.add_parser("delete", help="delete a scenario")
    c.add_argument("scenario_id", help="the scenario ID to remove")
    add_profile_switch(c)
    # List
    c = subparser.add_parser("list", help="list all scenarios")
    add_pretty_switch(c)
    add_profile_switch(c)
    # Details
    c = subparser.add_parser("details", help="retrieve details of a scenario")
    c.add_argument("scenario_id", help="the scenario ID to retrieve")
    add_pretty_switch(c)
    add_profile_switch(c)
    # Reload
    c = subparser.add_parser(
        "reload", help="trigger a reload of the existing scenarios"
    )
    add_profile_switch(c)
    # Apply
    c = subparser.add_parser(
        "apply", help="re-apply scenarios to the indicated works"
    )
    c. add_argument("work_id", nargs = '+')
    add_profile_switch(c)


def execute(args):
    """Executor"""
    config = Config()
    config.load_profile(args.profile)
    platform = Platform(config)
    if args.action == "add":
        if args.scenario_json == "-":
            scenario = json.load(sys.stdin)
        else:
            with open(args.scenario_json, "r", encoding="utf-8") as f:
                scenario = json.load(f)
        json_print(platform.add_scenario(scenario, args.replace_id), args.pretty)
    elif args.action == "delete":
        platform.delete_scenario(args.scenario_id)
        print("Scenario deleted")
    elif args.action == "list":
        json_print(platform.list_scenarios(), args.pretty)
    elif args.action == "details":
        json_print(platform.get_scenario(args.scenario_id), args.pretty)
    elif args.action == "reload":
        platform.reload_scenarios()
        print("Reload triggered")
    elif args.action == "apply":
        platform.apply_scenarios(args.work_id)
