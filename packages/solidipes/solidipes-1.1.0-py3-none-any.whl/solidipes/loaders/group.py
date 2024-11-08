import os
from abc import ABC, abstractmethod


class Group(ABC):
    """Group of files and directories."""

    def __init__(self, pattern: str, paths: list[str], **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def _find_groups(is_dir_path_dict: dict[str, bool]) -> dict[str, list[str]]:
        """Find groups of file and directory names.

        From a list of file and directory names (on a single level), return a
        dictionary with
        - key: pattern,
        - value: list of file and directory names that belong to the group.
        """


class LoaderList:
    """Lazily evaluated list of loaders"""

    def __init__(self):
        self._list = []

    def _populate_list(self):
        from .file_sequence import FileSequence

        # Note: the first matching type is used
        self._list = [
            FileSequence,
        ]

    def __iter__(self):
        if not self._list:
            self._populate_list()

        return iter(self._list)

    def __getitem__(self, item):
        if not self._list:
            self._populate_list()

        return self._list[item]


loader_list = LoaderList()


def load_groups(
    is_dir_path_dict: dict[str, bool],
    root_path: str,
) -> tuple[
    dict[str, Group],
    dict[str, bool],
]:
    """Load groups of files and directories.

    Return a dictionary of {pattern: loaded groups} and a dictionary with the
    remaining file and directory names.
    """

    loaded_groups = {}

    for loader in loader_list:
        # Find groups
        groups = loader._find_groups(is_dir_path_dict)

        # Load groups
        for pattern, names in groups.items():
            paths = [os.path.join(root_path, name) for name in names]
            loaded_group = loader(pattern=pattern, paths=paths)
            loaded_groups[pattern] = loaded_group

        # Remove file and directory names that are part of a new group
        for names in groups.values():
            for name in names:
                del is_dir_path_dict[name]

    remaining_is_dir_path_dict = is_dir_path_dict

    return loaded_groups, remaining_is_dir_path_dict
