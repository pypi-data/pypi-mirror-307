import argparse

import solidipes.uploaders
from solidipes.plugins.discovery import get_subclasses_from_package
from solidipes.uploaders.uploader import Uploader

command = "upload"
command_help = "Upload dataset to an online repository"


# Get all uploaders
uploader_subclasses = get_subclasses_from_package(solidipes.uploaders, Uploader)
uploader_subclasses_instances = [Subclass() for Subclass in uploader_subclasses]
uploaders = {uploader.command: uploader for uploader in uploader_subclasses_instances}


def main(args):
    platform = args.platform
    uploader = uploaders[platform]
    uploader.upload(args)


def populate_arg_parser(parser):
    # Create subparsers for each upload platform
    uploader_parsers = parser.add_subparsers(dest="platform", help="Target hosting platform")
    uploader_parsers.required = True

    for uploader in uploaders.values():
        uploader_parser = uploader_parsers.add_parser(uploader.command, help=uploader.command_help)
        uploader.populate_arg_parser(uploader_parser)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    populate_arg_parser(parser)
    args = parser.parse_args()
    main(args)
