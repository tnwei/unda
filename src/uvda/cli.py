import argparse

def handle_root(): pass;
def handle_list(): pass;
def handle_activate(): pass;
def handle_deactivate(): pass;

def entrypoint():
    parser = argparse.ArgumentParser(description="unda - manage arbitrary python envs like conda")
    subparsers = parser.add_subparsers(dest="whichsubcommand")

    list_parser = subparsers.add_parser("list")
    activate_parser = subparsers.add_parser("activate")
    deactivate_parser = subparsers.add_parser("deactivate")

    args = parser.parse_args()
    
    if args.whichsubcommand is None:
        handle_root()
    elif args.whichsubcommand == "list":
        handle_list()
    elif args.whichsubcommand == "activate":
        handle_activate()
    elif args.whichsubcommand == "deactivate":
        handle_deactivate()

