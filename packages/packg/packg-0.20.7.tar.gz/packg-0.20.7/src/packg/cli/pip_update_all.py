from pathlib import Path
from typing import Optional

from loguru import logger
from attrs import define

from packg.iotools import load_json, loads_json
from packg.log import SHORTEST_FORMAT, configure_logger, get_logger_level_from_args
from packg.system import systemcall_with_assert
from typedparser import VerboseQuietArgs, add_argument, TypedParser


@define
class Args(VerboseQuietArgs):
    pass


def main():
    parser = TypedParser.create_parser(Args, description=__doc__)
    args: Args = parser.parse_args()
    configure_logger(level=get_logger_level_from_args(args), format=SHORTEST_FORMAT)
    logger.info(f"{args}")

    jsondata, _, _ = systemcall_with_assert("pip list --format json")
    data = loads_json(jsondata)
    names = []
    for pkg in data:  # e.g. {"name": "a", "version": "3.1.2", " "editable_project_location": "..."}
        if "editable_project_location" in pkg:
            logger.warning(f"SKIP {pkg}")
            continue
        name = pkg["name"]
        names.append(name)
    final_cmd = f"pip install -U {' '.join(names)}"
    print()
    print(final_cmd)
    print()
    for name in names:
        print(F"pip install -U {name} --no-deps")
    print()


if __name__ == "__main__":
    main()
