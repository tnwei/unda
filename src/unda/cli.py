import argparse
import os
from pathlib import Path

SKIP_SCAN_DIRS = [".git", "node_modules", "__pycache__"]


def handle_list():
    path_env_string = os.getenv("UNDAPATH")
    python_env_dirs = []

    if path_env_string is not None:
        # os.path.sep != os.pathsep
        # https://stackoverflow.com/questions/1499019/how-to-get-the-path-environment-variable-separator-in-python
        paths = path_env_string.split(os.pathsep)

        for path in paths:
            python_env_dirs.extend(get_python_env_dirs(path, current_recursion_depth=0))

    else:
        # TODO: Does it make sense to set up a default?
        # Not working upon setup is a bit killjoy hmm
        print("UNDAPATH env var is not set! Exiting")
        return

    for path in python_env_dirs:
        print(path)


def handle_activate(env_path):
    # Found out that child processes cannot affect root env vars
    # Studied a bit, have to run as bash script! Damn
    # TODO: Continue by weighing bash shim like conda init or do whole thing in bash
    pass


def handle_deactivate():
    pass


def is_python_env(p: Path) -> bool:
    # Slightly unrelated, but VSCode autodiscovery relies on using a dedicated binary
    # and searching for known tools
    # https://code.visualstudio.com/docs/python/environments#_environment-discovery
    if not p.is_dir():
        return False
    if (p / "bin/activate").is_file() and (p / "bin/python").is_file():
        return True
    return False


def get_python_env_dirs(
    rootpath: str | Path, current_recursion_depth: int, max_recursion_depth: int = 5
):
    # W/o recursion limits, this is same time as conda env list on my machine, ~1s
    # With recursion limits = 5, this takes ~100ms according to `time`
    # I guess probability of a dir to be a python env decreases w depth?
    # Still, leaving a note to say that I eyeballed it
    results = []
    p = Path(rootpath).expanduser()
    if is_python_env(p):
        results.append(p)
        # Return early since envs dont nest
        return results

    if current_recursion_depth == max_recursion_depth:
        return results

    for child in p.iterdir():
        if child.name in SKIP_SCAN_DIRS:
            continue
        # Prevent accidentally looping with symlinks
        if child.is_dir() and not child.is_symlink():
            results.extend(
                get_python_env_dirs(
                    child,
                    current_recursion_depth=current_recursion_depth + 1,
                    max_recursion_depth=max_recursion_depth,
                )
            )

    return results


def entrypoint():
    parser = argparse.ArgumentParser(
        description="unda - manage arbitrary python envs like conda"
    )
    subparsers = parser.add_subparsers(dest="whichsubcommand")

    list_parser = subparsers.add_parser("list")
    activate_parser = subparsers.add_parser("activate")
    deactivate_parser = subparsers.add_parser("deactivate")

    # Positional arg but optional: https://stackoverflow.com/a/4480202
    activate_parser.add_argument("env_path", default=".", nargs="?")

    args = parser.parse_args()

    if args.whichsubcommand is None:
        parser.print_help()
    elif args.whichsubcommand == "list":
        handle_list()
    elif args.whichsubcommand == "activate":
        handle_activate(args.env_path)
    elif args.whichsubcommand == "deactivate":
        handle_deactivate()
