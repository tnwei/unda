import argparse

def entrypoint():
    parser = argparse.ArgumentParser(description="unda, manage arbitrary python envs like conda")
    subparsers = parser.add_subparsers()

    list_parser = subparsers.add_parser("list")
    activate_parser = subparsers.add_parser("activate")
    deactivate_parser = subparsers.add_parser("deactivate")

    args = parser.parse_args()

    print("Hello world!")
