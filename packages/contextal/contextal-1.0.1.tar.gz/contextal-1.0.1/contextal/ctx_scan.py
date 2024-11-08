import argparse
import io
import os
import sys
import time
import traceback
from contextal import Config, Platform
from contextal.misc import add_profile_switch

class ActionsConfig:
    def __init__(self, actions_priority, ignored_actions):
        action_list = actions_priority.split(",")
        if len(action_list) == 0:
            raise Exception("--actions-priority is empty")
        self.priority = {}
        priority = 0
        for action in action_list:
            self.priority[action] = {
                "priority": priority,
                "clean": False
            }
            priority = priority + 1
        ignored_list = ignored_actions.split(",")
        for action in ignored_list:
            if action not in self.priority:
                continue
            self.priority[action]["clean"]=True
    def get(self, action):
        if action not in self.priority:
            return None
        return self.priority[action]

class DirectoryInfo:
    def __init__(self, path, recursion):
        self.path = path
        self.recursion = recursion

class WorkInfo:
    def __init__(self, work_id, path):
        self.work_id = work_id
        self.path = path

def check_path(path):
    if os.path.isfile(path):
        return path
    if os.path.isdir(path):
        return DirectoryInfo(path, 0)
    raise Exception("Invalid path")


def initialize_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("path", help="file or directory to submit", type=check_path)
    parser.add_argument(
        "--recursive",
        help="scan directories recursively",
        action="store_true",
    )
    parser.add_argument(
        "--max-dir-recursion",
        help="maximum depth directories are scanned at",
        type=int,
        default=15,
    )
    parser.add_argument(
        "--ttl",
        help="number of seconds allowed to fully complete this work request (optional)",
        type=int,
        default=300
    )
    parser.add_argument(
        "--max-object-recursion",
        help="depth limit for processing nested objects",
        type=int,
    )
    parser.add_argument("--org", help="organization identifier")
    add_profile_switch(parser)
    parser.add_argument(
        "--actions-priority",
        default="ALLOW,BLOCK,QUARANTINE,ALERT,SPAM",
        help="the list of actions ordered from highest to lowest priority, which can be reported. Actions not listed here will be ignored"
        )
    parser.add_argument(
        "--ignored-actions",
        default="ALLOW",
        help='comma separated list of actions that should not be reported'
    )
    parser.add_argument(
        "--report-all",
        help="report all triggered actions. By default the highest priority action, which is not set as ignored, gets reported",
        action="store_true"
    )
    parser.add_argument(
        "-i", "--infected",
        help="print only infected files",
        action="store_true"
    )
    return parser

def list_actions(actions_array, ignored_actions, filepath, infected_only):
    empty = True
    for element in actions_array:
        actions = element["actions"]
        for action in actions:
            scenario=action["scenario"]
            action = action["action"]
            if infected_only and action in ignored_actions:
                continue
            empty = False
            print("{0}: Contextal-Action-{1}: {2}".format(filepath, action, scenario))
    if empty and not infected_only:
        print("{0}: No actions".format(filepath))

def scan_actions(actions_array, actions_config, filepath, infected_only):
    result = None
    for element in actions_array:
        actions = element["actions"]
        for action in actions:
            scenario=action["scenario"]
            action = action["action"]
            config = actions_config.get(action)
            if config is None:
                continue
            if result is None or config["priority"] < result["priority"]:
                result = {
                    "action": action,
                    "scenario": scenario,
                    "priority": config["priority"],
                    "clean": config["clean"]
                }
    if result is None or result["clean"]:
        if not infected_only:
            print("{}: Clean".format(filepath))
        return False
    else:
        print("{0}: Contextal-Action-{1}: {2}".format(filepath, result["action"], result["scenario"]))
        return True

def get_next_recursion(recursion, args):
    if not args.recursive:
        return None
    max = args.max_dir_recursion
    if max is not None and max <= recursion:
        return None
    return recursion + 1


def main():
    try:
        args = initialize_parser().parse_args()
        actions_config = ActionsConfig(args.actions_priority, args.ignored_actions)
        config = Config()
        config.load_profile(args.profile)
        platform = Platform(config)

        WORK_LIMIT = 3
        path_queue = []
        work_queue = []
        path_queue.append(args.path)
        any_infected = False

        while len(path_queue) > 0 or len(work_queue) > 0:
            sleep = True
            if len(work_queue) < WORK_LIMIT and len(path_queue) > 0:
                path = path_queue.pop(0)
                if isinstance(path, DirectoryInfo):
                    next_recursion = get_next_recursion(path.recursion, args)
                    dir_iter = os.scandir(path.path)
                    for entry in dir_iter:
                        if entry.is_file(follow_symlinks=False):
                            path_queue.append(entry.path)
                        elif entry.is_dir(follow_symlinks=False) and next_recursion is not None:
                            path_queue.append(DirectoryInfo(path=entry.path, recursion=next_recursion))
                    continue
                else:
                    stat = os.stat(path)
                    if stat.st_size == 0:
                        sys.stderr.write("{0}: Skipping empty file\n".format(path))
                        continue
                    file = open(path, "rb")
                    work_id = platform.submit_work(file, ttl=args.ttl, org=args.org, max_recursion=args.max_object_recursion)["work_id"]
                    work_queue.append(WorkInfo(work_id, path))
                    sleep = False
            work_id_array = []
            for work in work_queue:
                work_id_array.append(work.work_id)
            graphs = platform.get_graphs(work_id_array)
            finished = []
            for work in work_queue:
                if graphs[work.work_id] is not None:
                    finished.append(work)
                    sleep = False
                    filepath = work.path
                    actions_array = platform.get_actions(work.work_id)
                    if args.report_all:
                        list_actions(actions_array, args.ignored_actions, filepath, args.infected)
                    else:
                        infected = scan_actions(actions_array, actions_config, filepath, args.infected)
                        if infected:
                            any_infected = True
            for work in finished:
                work_queue.remove(work)
            if sleep:
                time.sleep(0.5)
        sys.exit(1 if any_infected else 0)
    except Exception as ex:
        traceback.print_exc()
        sys.exit(2)

if __name__ == "__main__":
    main()
