import os
from pathlib import Path
import argparse

def handle_root(): pass;

def handle_list(python_env_dirs: list[Path]):
    print(python_env_dirs)

def handle_activate(): pass;
def handle_deactivate(): pass;

def is_python_env(p: Path) -> bool:
    # Slightly unrelated, but VSCode autodiscovery relies on using a dedicated binary
    # and searching for known tools
    # https://code.visualstudio.com/docs/python/environments#_environment-discovery
    if not p.is_dir():
        return False
    if (p / "bin/activate").is_file() and (p / "bin/python").is_file():
        return True
    return False

def get_python_env_dirs(rootpath: str | Path):
    results = []
    p = Path(rootpath).expanduser()
    if is_python_env(p):
        results.append(p)
    for child in p.iterdir():
        # Prevent accidentally looping with symlinks
        if child.is_dir() and not child.is_symlink():
            results.extend(get_python_env_dirs(child))
    return results


def entrypoint():
    parser = argparse.ArgumentParser(description="unda - manage arbitrary python envs like conda")
    subparsers = parser.add_subparsers(dest="whichsubcommand")

    list_parser = subparsers.add_parser("list")
    activate_parser = subparsers.add_parser("activate")
    deactivate_parser = subparsers.add_parser("deactivate")

    args = parser.parse_args()

    path_env_string = os.getenv("UNDAPATH")
    python_env_dirs = []

    if path_env_string is not None:
        # os.path.sep != os.pathsep
        # https://stackoverflow.com/questions/1499019/how-to-get-the-path-environment-variable-separator-in-python
        paths = path_env_string.split(os.pathsep)

        for path in paths:
            python_env_dirs.append(get_python_env_dirs(path))

    else:
        # TODO: Does it make sense to set up a default?
        # Not working upon setup is a bit killjoy hmm
        print("UNDAPATH env var is not set! Exiting")
        return
    
    if args.whichsubcommand is None:
        handle_root()
    elif args.whichsubcommand == "list":
        handle_list(python_env_dirs)
    elif args.whichsubcommand == "activate":
        handle_activate()
    elif args.whichsubcommand == "deactivate":
        handle_deactivate()

