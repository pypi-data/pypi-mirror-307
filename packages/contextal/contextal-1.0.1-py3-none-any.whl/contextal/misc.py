"""
Miscellana
"""

import json
import typing


def json_print(item: typing.Any, pretty: bool = False):
    """Print JSON data in compact or pretty form"""
    if pretty:
        print(json.dumps(item, sort_keys=True, indent=4))
    else:
        print(json.dumps(item, separators=(",", ":")))


def add_profile_switch(parser):
    """Add --profile command line switch"""
    parser.add_argument("--profile", help="platform configuration profile to use")


def add_pretty_switch(parser):
    """Add --pretty command line switch"""
    parser.add_argument(
        "--pretty", help="pretty print JSON output", action="store_true"
    )
