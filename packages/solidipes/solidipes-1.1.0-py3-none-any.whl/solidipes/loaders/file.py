import os
from functools import cache
from typing import Optional, Type

from ..plugins.discovery import loader_list
from ..utils import get_mimes, get_path_relative_to_root
from ..utils import solidipes_logging as logging
from .cached_metadata import CachedMetadata
from .data_container import DataContainer
from .mime_types import get_extension, get_mime_type, get_possible_extensions, is_valid_extension

logger = logging.getLogger()


#: List of supported extensions per class
_supported_extensions = {}


class File(CachedMetadata, DataContainer):
    """Abstract container class for file metadata

    A File can be read from disk and may contain multiple DataContainer
    entries.
    """

    #: List of supported mime types. Override in subclasses.
    #: The key is the mime type and the value is one or more file extensions (string or list of strings)
    supported_mime_types = {}

    @classmethod
    def _supported_extensions(cls):
        name = cls.__name__
        if name in _supported_extensions:
            return _supported_extensions[name]
        _supported_extensions[name] = []

        if not isinstance(cls.supported_mime_types, dict):
            raise RuntimeError(f"need adapting class {cls}")
        for _, exts in cls.supported_mime_types.items():
            if isinstance(exts, str) or not isinstance(exts, list):
                exts = [exts]
            _supported_extensions[name] += exts
        _supported_extensions[name] = list(set(_supported_extensions[name]))
        return _supported_extensions[name]

    def __init__(self, path=None):
        if path is None:
            raise RuntimeError("File need a path to be initialized")

        logger.debug(f"Loading a file as data container {path}")
        self.path = path
        self._discussions = []
        self._archived_discussions = False
        super().__init__(
            unique_identifier=get_path_relative_to_root(path),
            name=os.path.basename(path),
        )

    @CachedMetadata.cached_property
    def modified_time(self):
        return os.path.getmtime(self.path)

    @CachedMetadata.cached_property
    def preferred_loader_name(self):
        return f"{self.__class__.__module__}.{self.__class__.__qualname__}"

    def add_message(self, author, msg):
        self._discussions = self.discussions
        self._discussions.append((author, msg))
        self.set_cached_metadata_entry("discussions", self._discussions)

    def archive_discussions(self, flag=True):
        self._archived_discussions = flag
        self.set_cached_metadata_entry("archived_discussions", self._archived_discussions)

    def _valid_loading(self):
        return super()._valid_loading() and self._valid_extension() and self._valid_non_empty()

    def _valid_non_empty(self):
        res = self.file_info.size > 0
        if not res:
            self.errors.append("Empty file")
        return res

    def _valid_extension(self):
        if self.file_info.path in get_mimes():
            return True

        res = is_valid_extension(self.file_info.path, self.file_info.type)

        if not res:
            self.errors.append(
                f"Mime type '{self.file_info.type}' not matching extension '{os.path.splitext(self.file_info.path)[1]}'"
            )
        return res

    @CachedMetadata.cached_loadable
    def discussions(self):
        return self._discussions

    @CachedMetadata.cached_loadable
    def archived_discussions(self):
        return self._archived_discussions

    @CachedMetadata.cached_loadable
    def valid_loading(self):
        return self._valid_loading()

    @DataContainer.loadable
    def file_stats(self):
        stats = os.stat(self.path)
        return stats

    @CachedMetadata.cached_loadable
    def file_info(self):
        stats = self.file_stats
        mime_type, charset = get_mime_type(self.path)
        return DataContainer({
            "size": stats.st_size,
            "changed_time": stats.st_ctime,
            "created_time": stats.st_ctime,
            "modified_time": stats.st_mtime,
            "permissions": stats.st_mode,
            "owner": stats.st_uid,
            "group": stats.st_gid,
            "path": self.path.strip(),
            "type": mime_type,
            "charset": charset.strip(),
            "extension": get_extension(self.path).strip(),
        })

    @classmethod
    @cache
    def check_file_support(cls, path):
        """Check mime type, then extension of file"""
        mime_type, _ = get_mime_type(path)

        if mime_type is None:
            logger.info(f"Invalid MIME for {path}: {mime_type}")
        for supported_mime_type in cls.supported_mime_types:
            if mime_type.startswith(supported_mime_type):
                return True

        extension = get_extension(path)

        if extension in cls._supported_extensions():
            return True

        extensions = get_possible_extensions(mime_type)
        for e in extensions:
            if e in cls._supported_extensions():
                return True

        return False


def load_file(path):
    """Load a file from path into the appropriate object type"""

    from solidipes_core_plugin.loaders.binary import Binary
    from solidipes_core_plugin.loaders.symlink import SymLink

    if os.path.islink(path):
        return SymLink(path=path)

    if not os.path.isfile(path):
        raise FileNotFoundError(f'File "{path}" does not exist')

    # Get cached preferred loader
    preferred_loader = get_cached_preferred_loader(path)

    if preferred_loader:
        try:
            obj = preferred_loader(path=path)
            for pref_type in preferred_loader.supported_mime_types:
                if obj.file_info.type.startswith(pref_type):
                    return obj
            if obj.file_info.extension in preferred_loader._supported_extensions():
                return obj

            if preferred_loader == Binary:
                return obj
        except RuntimeError as e:
            import streamlit as st

            st.error(f"Cannot load {type(path)}: {type(e)}")
            st.error(f"Cannot load {path}: {e}")
        logger.warning(
            "Cache miss:"
            f" {path} {preferred_loader} {preferred_loader.supported_mime_types}"
            f" {preferred_loader._supported_extensions()}"
        )

    # If no cached preferred loader, try to find a loader
    for loader in loader_list:
        if loader.check_file_support(path):
            try:
                return loader(path=path)
            except RuntimeError as e:
                import streamlit as st

                st.error(f"Cannot load {path}: {e}")

    # If no extension or unknown extension, assume binary
    return Binary(path=path)


def get_cached_preferred_loader(path: str) -> Optional[Type[File]]:
    """Get the preferred loader for a file from global cache"""

    from .cached_metadata import CachedMetadata

    unique_identifier = get_path_relative_to_root(path)
    preferred_loader_name = (
        CachedMetadata.get_global_cached_metadata().get(unique_identifier, {}).get("preferred_loader_name", None)
    )

    return loader_list.as_full_dict().get(preferred_loader_name, None)
