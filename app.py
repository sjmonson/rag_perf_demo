import argparse
from enum import Enum
from dotenv import load_dotenv
import os

from commands.chat import chat
from commands.import_data import import_data, clear_data

load_dotenv()


class Command(Enum):
    IMPORT_DATA = "import-data"
    CLEAR_DATA = "clear-data"
    CHAT = "chat"


def main():
    parser = argparse.ArgumentParser(description="Application Description")

    subparsers = parser.add_subparsers(
        title="Subcommands",
        dest="command",
        help="Display available subcommands",
    )

    # import-data command
    import_data_parser = subparsers.add_parser(
        Command.IMPORT_DATA.value, help="Import data"
    )
    import_data_parser.add_argument(
        "data_source", nargs='+', type=str, help="Specify the PDF data source"
    )
    import_data_parser.set_defaults(func=import_data)

    # Clear data
    clear_data_parser = subparsers.add_parser(
        Command.CLEAR_DATA.value, help="Clear data"
    )
    clear_data_parser.set_defaults(func=clear_data)

    # chat command
    chat_parser = subparsers.add_parser(
        Command.CHAT.value, help="Use chat feature"
    )
    chat_parser.set_defaults(func=chat)

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        print("Invalid command. Use '--help' for assistance.")


if __name__ == "__main__":
    main()
