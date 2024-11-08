"""
The "download" subcommand processor
"""

import os
import sys

from contextal.config import Config
from contextal.misc import add_profile_switch
from contextal.platform import Platform

ARG_CMD = "download"


def add_argparser(parser):
    """Subparser"""
    subparser = parser.add_parser(ARG_CMD, help="download object data")
    subparser.add_argument("object_id", help="ID of the object to download")
    subparser.add_argument(
        "output_file", help="file in which data is saved (use - for stdout)"
    )
    add_profile_switch(subparser)


def execute(args):
    """Executor"""
    config = Config()
    config.load_profile(args.profile)
    platform = Platform(config)
    response = platform.download_object(args.object_id)
    try:
        if args.output_file == "-":
            output = sys.stdout.buffer
        else:
            output = open(args.output_file, "wb")
        for chunk in response.iter_content(chunk_size=4096):
            output.write(chunk)
        output.flush()
    except Exception:
        if args.output_file != "-":
            try:
                os.unlink(args.output_file)
            except Exception:
                pass
        raise
    finally:
        if args.output_file != "-":
            output.close()
