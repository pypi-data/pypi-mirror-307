import argparse
import fnmatch
import os

from solidipes.loaders.file import load_file
from solidipes.loaders.mime_types import get_possible_extensions
from solidipes.reports.report import Report
from solidipes.scanners.scanner import Scanner
from solidipes.utils import bcolors, get_path_relative_to_root, logging, rename_file

print = logging.invalidPrint
logger = logging.getLogger()


################################################################


class CurationReport(Report):
    command = "curation"
    command_help = "Generate a curation report for a file or directory"

    def make(self, args: argparse.Namespace):
        logger.info(f'Generating curation report for "{args.path}"')

        if os.path.isfile(args.path):
            self.scan_file(args.path, rename=args.rename, open_errors=args.open)

        else:
            self.scan_directories(
                dir_path=args.path,
                file_wildcard=args.file_wildcards,
                rename=args.rename,
                open_errors=args.open,
            )

    def populate_arg_parser(self, parser: argparse.ArgumentParser):
        parser.description = self.command_help

        parser.add_argument(
            "path",
            nargs="?",
            default=".",
            help="Path to the file or directory to generate the report for. Defaults to current directory",
        )

        parser.add_argument(
            "--file-wildcards",
            metavar="file_wildcards",
            help="Filter files to curate",
            default="*",
        )

        parser.add_argument(
            "--rename",
            help="Automatically rename files with extension not matching their mimetype",
            action="store_true",
        )

        parser.add_argument(
            "--open",
            help="Try to view files with errors",
            action="store_true",
        )

    def scan_file(self, file_path, **kwargs):
        loader = load_file(file_path)
        self.display_file(loader, **kwargs)

    def scan_directories(self, dir_path, **kwargs):
        scanner = Scanner(dir_path)
        loaders = scanner.get_loader_dict()

        for loader in loaders.values():
            self.display_file(loader, **kwargs)

    def display_file(self, e, file_wildcard="*", rename=False, open_errors=False):
        path = e.path
        if not fnmatch.fnmatch(e.file_info.path, file_wildcard):
            return

        display_path = f"{get_path_relative_to_root(path)}"

        if e.valid_loading:
            message = f"{display_path}: {bcolors.BRIGHT_GREEN}OK{bcolors.RESET}"
            logger.info(message)

        else:
            message = f"{bcolors.BRIGHT_RED}{display_path}:1: "
            message += f"{len(e.errors)} ERROR"

            if len(e.errors) > 1:
                message += "S"

            for error in e.errors:
                message += f"\n{error}"

            message += f"{bcolors.RESET}\n"
            logger.error(message)

            if open_errors:
                logger.info(f"{bcolors.BRIGHT_RED}Opening file...{bcolors.RESET}")
                e.view()

            if rename:
                old_name = path
                ext = get_possible_extensions(e.file_info.type)[0]
                new_name = os.path.splitext(old_name)[0] + "." + ext
                logger.info(f"{bcolors.BRIGHT_YELLOW}Renaming file {old_name} to {new_name}{bcolors.RESET}")
                rename_file(old_name, new_name)
