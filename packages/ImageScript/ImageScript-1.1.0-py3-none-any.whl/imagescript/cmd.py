import re
from argparse import ArgumentParser
from getpass import getpass
from pathlib import Path

from imagescript.converter import Converter

__version__ = "1.1.0"


def _get_base_parser() -> ArgumentParser:
    base_parser = ArgumentParser(add_help=False)
    base_parser.add_argument(
        "-P",
        help="A flag that a password is to be used for AES encryption/decryption. "
            "This flag will open a secure password prompt.",
        action="store_true",
        default=False,
        dest="password_flag"
    )
    base_parser.add_argument(
        "--password",
        help="Directly supply a password to be used for AES encryption/decryption. (UNSAFE) "
            "Encryption is automatically executed if a password is supplied."
    )
    base_parser.add_argument("target_file", help="The image or text file to operate on.", type=Path)
    base_parser.add_argument(
        "-o",
        "--output",
        help="The output file to write to. "
            "If not specified the same file with a '.out' extension will be created at the target location.",
        type=Path
    )
    base_parser.add_argument(
        "-f", "--force", help="Do not prevent overwriting of files", action="store_true", default=False
    )
    return base_parser


def main():
    parser = ArgumentParser(
        prog="imagescript",
        description="A command line tool to convert text into images and back. Also supports executing images as "
                    "scripts and basic Steganography with pack and unpack."
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"ImageScript v{__version__}",
        help="Print the version number and exit.",
    )
    subparsers = parser.add_subparsers(title="command", help="The command to execute.", required=True, dest="command")

    base_parser = _get_base_parser()

    # Add to_image parser
    to_image_parser = subparsers.add_parser("to_image", help="Convert text to an image.", parents=[base_parser])
    to_image_parser.add_argument(
        "-a",
        "--aspect-ratio",
        help="The aspec ratio to use for the image. Format: x:y (16:9)",
        type=str,
        dest="aspect_ratio",
        default="1:1"
    )

    # Add to_text parser
    subparsers.add_parser("to_text", help="Convert image to a text.", parents=[base_parser])

    # Add execute parser
    exec_parser = subparsers.add_parser(
        "execute",
        help="Execute an image file containing a python script. Be careful when using this command."
            "Do not execute scripts from unknown sources!",
        parents=[base_parser]
    )
    exec_parser.add_argument("--arg", help="An argument to pass to the executed script", action="append")

    # Add pack parser
    pack_parser = subparsers.add_parser(
        "pack", help="Pack a text file into an image. (Steganography)", parents=[base_parser]
    )
    pack_parser.add_argument("cover_image", help="The cover image used to hide the data.", type=Path)

    # Add unpack parser
    subparsers.add_parser(
        "unpack", help="Extract text from an image file. (Steganography)", parents=[base_parser]
    )

    args = parser.parse_args()
    if not args.target_file.is_file():
        raise FileNotFoundError(f"The target file '{args.target_file}' does not exist.")

    if not args.output:
        args.output = args.target_file
    elif args.output.is_dir():
        args.output = args.output / args.target_file.name

    if args.password_flag:
        args.password = getpass("Enter a password: ")

    match args.command:
        case "to_image":
            if not re.match(r"^\d+:\d+$", args.aspect_ratio):
                raise ValueError("The aspect ratio must be in the format x:y (16:9)")
            size: tuple[int, int] = tuple(int(r) for r in reversed(args.aspect_ratio.split(":"))) # type: ignore
            Converter.file_to_image(args.target_file, size, args.output, args.force, args.password)
        case "to_text":
            Converter.image_to_file(args.target_file, args.output, args.force, args.password)
        case "execute":
            Converter.execute_image(args.target_file, args.arg, args.password)
        case "pack":
            Converter.pack(args.target_file, args.cover_image, args.output, args.force, args.password)
        case "unpack":
            Converter.unpack(args.target_file, args.output, args.force, args.password)

if __name__ == "__main__":
    main()
