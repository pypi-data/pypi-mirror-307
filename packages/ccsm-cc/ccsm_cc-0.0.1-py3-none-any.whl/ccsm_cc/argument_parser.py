from dataclasses import dataclass
from pathlib import Path
import sys
import argparse
from typing import Optional


@dataclass
class Args:
    main_path: Path
    import_path: Optional[Path]


def parse_args() -> Args:
    parser = argparse.ArgumentParser(
        prog=f"{sys.executable} -m ccsm",
        description="A WIP Save Manager for Crab Champions",
    )
    parser.add_argument(
        "-p",
        "--path",
        help="the path of CCSM's internal files",
        type=Path,
        default=Path.home(),
        dest="main"
    )
    parser.add_argument("-i", "--import", help="Import a .sav file", type=Path, dest="sav")
    args = parser.parse_args()
    return Args(args.main, args.sav)
