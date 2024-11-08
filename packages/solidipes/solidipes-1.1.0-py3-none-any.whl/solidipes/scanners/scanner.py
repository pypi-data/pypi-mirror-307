import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Optional, Protocol, Set, Union

from tqdm import tqdm

from ..loaders.file import File, load_file
from ..loaders.group import Group, load_groups
from ..utils import default_ignore_patterns, get_ignore, logging, solidipes_dirname

################################################################


print = logging.invalidPrint
logger = logging.getLogger()

################################################################


class DictTree(dict):
    def __init__(self, *args, **kwargs):
        """A nested dictionary that counts the number of leaves under each node."""

        super().__init__(*args, **kwargs)

        # Convert all nested dictionaries to DictTree
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = DictTree(value)

        self.count = self.count_leaves()

    def count_leaves(self) -> int:
        """Count the number of leaves in the tree."""

        count = 0

        for value in self.values():
            if isinstance(value, DictTree):
                count += value.count
            else:
                count += 1

        return count

    def flatten(
        self,
        value_func: Callable = lambda value: value,
        keys_join_func: Callable[[list[str]], str] = lambda keys: os.path.join(*keys),
        add_dicts: bool = False,
        dict_func: Callable = lambda _: None,
        keys: list[str] = [],
    ) -> dict:
        """Flatten the tree into a flat dictionary."""

        flattened = {}

        if add_dicts:
            joined_keys = keys_join_func(keys) if len(keys) > 0 else "."
            flattened[joined_keys] = dict_func(self)

        for key, value in sorted(self.items()):
            new_keys = keys + [key]
            joined_keys = keys_join_func(new_keys)

            if isinstance(value, DictTree):
                flattened.update(
                    value.flatten(
                        value_func=value_func,
                        keys_join_func=keys_join_func,
                        add_dicts=add_dicts,
                        dict_func=dict_func,
                        keys=new_keys,
                    )
                )

            else:
                flattened[joined_keys] = value_func(value)

        return flattened

    def filter(
        self,
        value_filter: Callable = lambda _: True,
        keys_join_func: Callable[[list[str]], str] = lambda keys: os.path.join(*keys),
        joined_keys_filter: Callable = lambda _: True,
        keep_empty_dicts: bool = False,
        keys: list[str] = [],
    ) -> "DictTree":
        """Filter the tree based on the values and keys. Both filters must be satisfied."""

        filtered = DictTree()

        for key, value in sorted(self.items()):
            new_keys = keys + [key]
            joined_keys = keys_join_func(new_keys)

            if isinstance(value, DictTree):
                sub_tree = value.filter(
                    value_filter=value_filter,
                    keys_join_func=keys_join_func,
                    joined_keys_filter=joined_keys_filter,
                    keep_empty_dicts=keep_empty_dicts,
                    keys=new_keys,
                )

                if len(sub_tree) > 0 or keep_empty_dicts:
                    filtered[key] = sub_tree

            elif value_filter(value) and joined_keys_filter(joined_keys):
                filtered[key] = value

        return filtered

    def apply(
        self,
        func: Callable,
    ) -> "DictTree":
        """Apply a function to all values in the tree."""

        applied = DictTree()

        for key, value in self.items():
            if isinstance(value, DictTree):
                applied[key] = value.apply(func)
            else:
                applied[key] = func(value)

        return applied

    def reduce(
        self,
        func: Callable,
        initial: Any,
    ) -> Any:
        """Reduce the tree to a single value."""

        acc = initial

        for value in self.values():
            if isinstance(value, DictTree):
                acc = value.reduce(func, acc)
            else:
                acc = func(acc, value)

        return acc


Loader = Union[File, Group]
FilepathTree = DictTree  # dict[str, "FilepathTree | str"]
LoaderTree = DictTree  # dict[str, "LoaderTree | Loader"]


class ProgressBar(Protocol):
    total: float

    def update(self, n: Optional[float]) -> Optional[bool]: ...
    def set_postfix_str(self, desc: str) -> None: ...
    def reset(self) -> None: ...
    def close(self) -> None: ...


class StreamlitProgressBar(ProgressBar):
    def __init__(self, text, container=None):
        import streamlit as st

        if container is None:
            container = st

        self.st_bar = container.progress(0, text=text)
        self.text = text
        self.total = 0
        self.current = 0
        self.postfix = ""

    def update(self, value):
        self.current += value
        self._update()

    def set_postfix_str(self, desc: str):
        self.postfix = desc
        self._update()

    def _update(self):
        text = f"{self.text} ({self.current}/{self.total}) {self.postfix}"
        self.st_bar.progress(100 * self.current // self.total, text=text)

    def reset(self):
        self.current = 0

    def close(self):
        self.st_bar.empty()


def cached_scan(func: Callable) -> Callable:
    """Decorator to cache the result of the scan.

    Adds a "force_rescan" parameter to the decorated function.
    Assumes that the result of the scan only depends on root_path and excluded_patterns.
    """

    @lru_cache(maxsize=1)
    def cached_func(self, root_path: str, excluded_patterns: frozenset[str], *args, **kwargs):
        logger.debug(f"Scanning with {func.__name__}")
        return func(self, *args, **kwargs)

    def wrapper(self, *args, force_rescan: bool = False, **kwargs):
        if force_rescan:
            cached_func.cache_clear()

        return cached_func(self, self.root_path, frozenset(self.excluded_patterns), *args, **kwargs)

    return wrapper


class Scanner:
    """A class to scan a directory to load files and groups.

    All paths are given relative to the scanner's root path.
    """

    def __init__(self, root_path: str = "."):
        self.root_path = root_path
        try:
            # Get ignored patterns from .solidipes
            self.excluded_patterns = get_ignore()
        except FileNotFoundError:
            self.excluded_patterns = default_ignore_patterns.copy()

        self.progress_bar: Optional[ProgressBar] = None

    @cached_scan
    def get_filepath_tree(self) -> FilepathTree:
        """Get a tree of all filepaths, organized by directory."""

        tree = {}

        for root, dirs, files in os.walk(self.root_path):
            dirpath = os.path.relpath(root, self.root_path)

            if self.is_excluded(dirpath):
                logger.debug(f"Exclude {dirpath}")
                dirs.clear()
                continue

            # Create the directory structure in the tree
            current_tree = tree
            for dirname in dirpath.split(os.sep):
                if dirname == ".":
                    continue

                if dirname not in current_tree:
                    current_tree[dirname] = {}

                current_tree = current_tree[dirname]

            # Add filepaths to the tree
            for file in files:
                filepath = os.path.relpath(os.path.join(dirpath, file))

                if self.is_excluded(filepath):
                    logger.debug(f"Exclude {filepath}")
                    continue

                current_tree[file] = filepath

        return DictTree(tree)

    @cached_scan
    def get_dirpath_tree(self) -> FilepathTree:
        """Get a tree of all directory paths."""

        return self.get_filepath_tree().filter(
            value_filter=lambda _: False,
            keep_empty_dicts=True,
        )

    @cached_scan
    def get_path_list(self) -> list[str]:
        """Get a list of all paths (files and directories)."""

        return list(
            self.get_filepath_tree()
            .flatten(
                value_func=lambda _: None,
                add_dicts=True,
            )
            .keys()
        )

    @cached_scan
    def get_filepath_list(self) -> list[str]:
        """Get a list of all file paths."""

        return list(
            self.get_filepath_tree()
            .flatten(
                value_func=lambda _: None,
            )
            .keys()
        )

    @cached_scan
    def get_loader_tree(
        self,
    ) -> LoaderTree:
        """Get a tree of loaders, with groups, organized by directory."""

        using_self_progress_bar = False

        if self.progress_bar is None:
            using_self_progress_bar = True
            self.progress_bar = tqdm(desc="Loading files")

        tree = self.get_filepath_tree()
        self.progress_bar.total = tree.count
        self.progress_bar.reset()
        tree = DictTree(
            convert_filepath_tree_to_loader_tree(
                tree=tree,
                root_path=self.root_path,
                progress_bar=self.progress_bar,
            )
        )

        self.progress_bar.close()

        if using_self_progress_bar:
            self.progress_bar = None

        return tree

    def get_filtered_loader_tree(
        self,
        dirs: list[str] = [],
        recursive: bool = True,
    ) -> LoaderTree:
        """Get a tree of loaders for the given directories."""

        if recursive:

            def path_filter(path: str):
                return any(path.startswith(d) for d in dirs)

        else:

            def path_filter(path: str):
                return os.path.dirname(path) in dirs

        return self.get_loader_tree().filter(
            joined_keys_filter=path_filter,
        )

    @cached_scan
    def get_loader_dict(
        self,
    ) -> dict[str, Loader]:
        """Get a dictionary mapping paths (potentially grouped) to loaders."""

        return self.get_loader_tree().flatten()

    def get_filtered_loader_dict(
        self,
        dirs: list[str] = [],
        recursive: bool = True,
    ) -> dict[str, Loader]:
        """Get a dictionary mapping paths (potentially grouped) to loaders."""

        return self.get_filtered_loader_tree(dirs, recursive=recursive).flatten()

    @cached_scan
    def get_loader_path_list(
        self,
    ) -> list[str]:
        """Get a list of all loaded paths (potentially grouped)."""

        return list(self.get_loader_dict().keys())

    def scan(self):
        """Trigger the creation of loaders."""

        self.get_loader_tree()

    def is_excluded(self, path: str, excluded_patterns: Optional[Set[str]] = None) -> bool:
        """Check whether the provided path is excluded by any of the scanner's patterns"""

        if excluded_patterns is None:
            excluded_patterns = self.excluded_patterns

        p = Path(path)

        for pattern in excluded_patterns:
            if pattern == ".":
                return True

            # If the pattern ends with a trailing slash, test whether the path is a directory
            if pattern.endswith("/"):
                if p.match(pattern) and p.is_dir():
                    return True

            # Otherwise, only test whether the path matches the pattern
            else:
                if p.match(pattern):
                    return True

        return False

    @cached_scan
    def get_modified_time(
        self,
    ) -> float:
        """Get the most recent modified time of all files."""

        return self.get_filepath_tree().reduce(
            func=lambda acc, value: max(acc, os.path.getmtime(value)),
            initial=0,
        )

    @cached_scan
    def get_total_size(
        self,
    ) -> int:
        """Get the total size of all files."""

        return self.get_filepath_tree().reduce(
            func=lambda acc, value: acc + os.path.getsize(value),
            initial=0,
        )


class ExportScanner(Scanner):
    """A scanner that keeps the .solidipes directory. Individual paths inside .solidipes can still be excluded."""

    def __init__(self, root_path: str = "."):
        super().__init__(root_path)

        if solidipes_dirname in self.excluded_patterns:
            self.excluded_patterns.remove(solidipes_dirname)

    def is_excluded(self, path: str, excluded_patterns: Optional[Set[str]] = None) -> bool:
        """Check whether the provided path is excluded by any of the scanner's patterns"""

        if excluded_patterns is None:
            excluded_patterns = self.excluded_patterns

        # Create a set of excluded patterns specific to the .solidipes directory
        # Typically: removes `.*` from the set of excluded patterns
        if solidipes_dirname in path:
            solidipes_excluded_patterns = set()

            for pattern in excluded_patterns:
                if solidipes_dirname in pattern and pattern != solidipes_dirname:
                    solidipes_excluded_patterns.add(pattern)

        else:
            solidipes_excluded_patterns = excluded_patterns

        return super().is_excluded(path, solidipes_excluded_patterns)


def convert_filepath_tree_to_loader_tree(
    tree: FilepathTree,
    root_path: str,
    progress_bar: Optional[ProgressBar] = None,
) -> LoaderTree:
    """Convert a tree of filepaths to a tree of loaders, while detecting file groups."""

    loaders = {}

    if progress_bar is not None:
        progress_bar.set_postfix_str(root_path)

    # Load groups
    is_dir_path_dict = {key: isinstance(value, dict) for key, value in tree.items()}
    loaded_groups, remaining_is_dir_path_dict = load_groups(is_dir_path_dict, root_path)
    loaders.update(loaded_groups)

    # Update progressbar for groups
    if progress_bar is not None:
        processed = set(tree.keys()) - set(remaining_is_dir_path_dict.keys())
        for key in processed:
            if isinstance(tree[key], DictTree):
                progress_bar.update(tree[key].count)
            else:
                progress_bar.update(1)

    # Load files
    filenames = [name for name, is_dir in is_dir_path_dict.items() if not is_dir]
    for name in filenames:
        if progress_bar is not None:
            progress_bar.set_postfix_str(os.path.join(root_path, name))
        filepath = os.path.join(root_path, name)
        loaders[name] = load_file(filepath)

        if progress_bar is not None:
            progress_bar.update(1)

    # Load subdirectories
    dirnames = {name for name, is_dir in is_dir_path_dict.items() if is_dir}
    for dirname in dirnames:
        subdir_tree: FilepathTree = tree[dirname]  # type: ignore
        subdir_root_path = os.path.join(root_path, dirname)
        subdir_loaders = convert_filepath_tree_to_loader_tree(
            tree=subdir_tree,
            root_path=subdir_root_path,
            progress_bar=progress_bar,
        )
        loaders[dirname] = subdir_loaders

    return loaders


def list_files(found, current_dir=""):
    items = []
    for k, v in found.items():
        full_dir = os.path.join(current_dir, k)
        items.append((full_dir, v))
        if isinstance(v, dict):
            items += list_files(v, current_dir=full_dir)
    return items
