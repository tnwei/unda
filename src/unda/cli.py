import argparse
import os
from pathlib import Path

SKIP_SCAN_DIRS = [".git", "node_modules", "__pycache__"]
SUPPORTED_SHELLS = ["bash"]


def get_all_python_env_dirs_in_undapath():
    # UNDAPATH is folder to recursively scan for python envs!
    path_env_string = os.getenv("UNDAPATH")
    python_env_dirs = []

    if path_env_string is not None:
        # os.path.sep != os.pathsep
        # https://stackoverflow.com/questions/1499019/how-to-get-the-path-environment-variable-separator-in-python
        paths = path_env_string.split(os.pathsep)

        for path in paths:
            python_env_dirs.extend(
                get_python_env_dirs(
                    # Make max_recursion_depth configurable or nay? hmmm
                    path,
                    current_recursion_depth=0,
                    max_recursion_depth=5,
                )
            )
        return python_env_dirs

    else:
        # TODO: Does it make sense to set up a default?
        # Not working upon setup is a bit killjoy hmm
        print("UNDAPATH env var is not set! Exiting")
        return []


def handle_list():
    python_env_dirs = get_all_python_env_dirs_in_undapath()
    for count, path in enumerate(python_env_dirs):
        print(f"{count + 1:02d}: {path}")


def handle_init(shell):
    """Define a bash fxn unda() that intercepts specific subcmds to run in bash instead of python"""
    if shell not in SUPPORTED_SHELLS:
        print(
            f"Your shell '{shell}' is not among the supported list: {','.join(SUPPORTED_SHELLS)}"
        )
        return

    if shell == "bash":
        # Thanks to https://learnxinyminutes.com/bash/
        # Test this fxn like by running `eval $(unda init bash)` then do unda commands
        # Make sure no need to use `uv run` locally in dev by using `uv tool install --editable .`
        print(r"""
# Unset existing bash fxns called unda
unset unda
# Store current unda exe name to prevent unda the bash fxn wanting to call unda the python script
# but inadvertently calls itself in an infinite loop!
UNDA_EXE=$(which unda)
unda() {
    case $1 in
        "")
        $UNDA_EXE
        # Return from the function without closing the interactive shell.
        return 0
        ;;
        hello) echo HELLO WORLD! ;;
        activate) eval "$("$UNDA_EXE" shell bash activate "$2")";;
        deactivate) deactivate;;
        *) $UNDA_EXE "$@";;
    esac
}
""")


def handle_shell(shell: str, command: list[str]):
    # Why do we have `unda init` to pass bash commands into `unda shell $SHELL $COMMAND`,
    # which then passes bash code back to be evaluated?
    # why do bash to python to bash?
    # Coz simple things like activate and deactivate python envs change bash env
    # When we run a python process from bash, it is spawned as a subprocess of that bash instance
    # Python can modify its own env but not its parent
    # So we need to run bash commands in bash
    # This setup allows most of the logic to be in Python and leave the bash bit thin
    if shell not in SUPPORTED_SHELLS:
        print(
            f"Your shell '{shell}' is not among the supported list: {','.join(SUPPORTED_SHELLS)}"
        )
        return

    if shell == "bash":
        return handle_shell_bash(command)


def can_int(x):
    try:
        int(x)
        return True
    except ValueError:
        return False


def handle_shell_bash(command) -> None:
    bash_payload = ""

    # The really nice bit about using native python source /bin/activate and deactivate
    # is that deactivate is a single word command
    # and we get the PS1 change from activating the env for free!
    if command[0] == "activate":
        if len(command) == 1:
            # no env to activate, print error msg
            print("echo activate requires path of python env to activate!")
        elif len(command) == 2:
            # have env to activate! resolve the env then print bash cmd
            env_to_activate = command[1]

            if can_int(env_to_activate):
                # if can be int'ed, then is a number to lookup from list of envs
                num_env_to_activate = int(env_to_activate) - 1
                python_env_dirs = get_all_python_env_dirs_in_undapath()
                resolved_env = python_env_dirs[num_env_to_activate]
            else:
                # cannot be int'ed, match against known envs
                raise NotImplementedError(
                    # TODO
                    "Please provide the env number from unda list! Matching env by name is not implemented yet"
                )

            bash_payload = f"source {resolved_env}/bin/activate"
    elif command[0] == "deactivate":
        bash_payload = "deactivate"

    # Note: how to make multiline payloads work? Rn only the first line gets run
    print(bash_payload)


def is_python_env(p: Path) -> bool:
    """
    Checks if the path is a Python env directory
    """
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

    init_parser = subparsers.add_parser("init")
    init_parser.add_argument(
        "shell",
        default="bash",
        help=f"Terminal shell. Supported: {','.join(SUPPORTED_SHELLS)}",
    )

    shell_parser = subparsers.add_parser("shell")
    shell_parser.add_argument(
        "shell",
        default="bash",
        help=f"Terminal shell. Supported: {','.join(SUPPORTED_SHELLS)}",
    )
    # Positional arg but optional: https://stackoverflow.com/a/4480202
    # nargs='*' means 0 to multiple commands, works by returning a list of strings!
    shell_parser.add_argument("command", nargs="*")

    args = parser.parse_args()

    if args.whichsubcommand is None:
        parser.print_help()
    elif args.whichsubcommand == "list":
        # uvda list
        # should show all python envs findable in UNDAPATH
        handle_list()
    elif args.whichsubcommand == "init":
        # uvda init $SHELL
        # append the following line to ~/.bashrc:
        # eval $(uvda init bash)
        handle_init(args.shell)
    elif args.whichsubcommand == "shell":
        # uvda shell $SHELL $command
        # Receives commands defined in the bash fxn from uvda init
        # shell should handle unda activate, unda deactivate
        handle_shell(args.shell, args.command)
