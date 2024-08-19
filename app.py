import argparse
from enum import Enum
from dotenv import load_dotenv
import os
import torch

from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

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
        if torch.cuda.is_available():
            device = "cuda"
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16
            )
        else:
            device = "cpu"
            bnb_config = None

        tokenizer = AutoTokenizer.from_pretrained(
            os.getenv("EMBED_TOKEN"),
            token=os.getenv("HF_TOKEN"),
        )
        model = AutoModelForCausalLM.from_pretrained(
            os.getenv("EMBED_MODEL"),
            token=os.getenv("HF_TOKEN"),
            quantization_config=bnb_config,
            device_map=device,
            torch_dtype=torch.float16,
        )

        args.func(args, model, device, tokenizer)
    else:
        print("Invalid command. Use '--help' for assistance.")


if __name__ == "__main__":
    main()
