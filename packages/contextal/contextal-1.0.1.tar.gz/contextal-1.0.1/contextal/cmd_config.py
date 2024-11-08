"""
The "config" subcommand processor
"""

from getpass import getpass
from contextal.config import Config
from contextal.platform import Platform

ARG_CMD = "config"


def add_argparser(parser):
    """Subparser"""
    subparser = parser.add_parser(
        ARG_CMD, help="manage platform configuration profiles"
    ).add_subparsers(dest="action", help="available actions:", required=True)
    # Create
    c = subparser.add_parser(
        "create", help="add (or replace) a platform configuration profile"
    )
    c.add_argument("profile", help="name of the profile to add")
    c.add_argument("url", help="platform URL")
    c.add_argument(
        "--token",
        help="platform Bearer token (optional)",
        nargs="?",
        const="",
    )
    c.add_argument(
        "--set-default",
        help="set this as the default profile",
        action="store_true",
    )
    c.add_argument(
        "--skip-test",
        help="add the profile without testing the platform reachability",
        action="store_true",
    )
    # Delete
    c = subparser.add_parser("delete", help="remove a platform configuration profile")
    c.add_argument("profile", help="name of the profile to add")
    # List
    subparser.add_parser("list", help="list platform configuration profiles")
    # Set-default
    c = subparser.add_parser(
        "set-default",
        help="set the specified platform configuration as the default profile",
    )
    c.add_argument("profile", help="name of the profile to add")


def execute(args):
    """Executor"""
    config = Config()
    if args.action == "create":
        if args.token == "":
            token = getpass("Please enter the authentication Bearer token: ")
        else:
            token = args.token
        if not args.skip_test:
            try:

                class TestConfig:
                    def platform(self) -> (str, str):
                        return (args.url, token)

                platform = Platform(TestConfig())
                platform.search('work_id=""', False, 1)
            except Exception as exc:
                raise ValueError(
                    "Failed to communicate with platform, please check your input"
                ) from exc
        config.write_profile(args.profile, args.url, token, args.set_default)
    elif args.action == "delete":
        if config.delete_profile(args.profile):
            print("Profile deleted")
        else:
            print("Profile not found")
    elif args.action == "list":
        profiles, default = config.list()
        if profiles:
            print("Available profiles:")
            for p in profiles:
                print("{} {}".format("*" if p == default else "-", p))
        else:
            print("No configured profiles found")
    elif args.action == "set-default":
        config.set_default(args.profile)
