import atexit
import os
import sched
import time

import transaction
import ZODB
import ZODB.FileStorage
from BTrees.OOBTree import BTree
from zc.lockfile import LockError

from ..utils import solidipes_logging as logging
from ..utils.config import cached_metadata_polling_interval, cached_metadata_polling_tries, cached_metadata_save_every
from ..utils.utils import (
    get_config,
    get_config_path,
    set_config,
    transform_data_containers_to_dict,
    transform_dict_to_data_containers,
)
from .data_container import DataContainer

print = logging.invalidPrint
logger = logging.getLogger()


class cached_property(property):
    """Decorator class to indicate that a property must be cached"""


class cached_loadable(DataContainer.loadable):
    """Decorator class to indicate that a loadable must be cached"""

    def __init__(self, func):
        super().__init__(func)

    def foo(self, obj, *args, **kwargs):
        data = DataContainer.loadable.foo(self, obj, *args, **kwargs)
        obj.set_cached_metadata_entry(self.key, data)
        return data

    def foo_setter(self, obj, value, *args, **kwargs):
        DataContainer.loadable.foo_setter(self, obj, value, *args, **kwargs)
        obj.save_field_to_cache(self.key)


_default_cached_attributes = {}
"List of @cached_property and @cached_loadable in the class"


class CachedMetadata(DataContainer):
    _storage = None
    _transaction_manager = transaction.TransactionManager()
    _global_cached_metadata = None
    _scheduler = sched.scheduler()
    _scheduled_commit = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cached_attributes = self._get_default_cached_attributes().copy()
        self.load_cached_metadata()

    def _get_default_cached_attributes(self) -> set:
        """Build the list of cached fields from the class description"""

        # Cannot be done on the instance because checking the loadable fields would trigger loading
        cls = self.__class__
        cls_name = cls.__name__

        if cls_name in _default_cached_attributes:
            return _default_cached_attributes[cls_name]

        _default_cached_attributes[cls_name] = set()

        for attribute_name in dir(cls):
            attribute = getattr(cls, attribute_name)

            if isinstance(attribute, cached_property) or isinstance(attribute, cached_loadable):
                _default_cached_attributes[cls_name].add(attribute_name)

        return _default_cached_attributes[cls_name]

    def clear_cached_metadata(self, fields=[]):
        if self.unique_identifier not in self.global_cached_metadata:
            return

        if fields:
            for field in fields:
                if field in self.global_cached_metadata[self.unique_identifier]:
                    del self.global_cached_metadata[self.unique_identifier][field]
            self.update_global_cached_metadata(self.unique_identifier)

        else:
            del self.global_cached_metadata[self.unique_identifier]

    def get_cached_metadata(self):
        if self.unique_identifier not in self.global_cached_metadata:
            self.global_cached_metadata[self.unique_identifier] = {}

        return self.global_cached_metadata[self.unique_identifier]

    @cached_property
    def modified_time(self):
        raise NotImplementedError

    def is_cache_invalid(self):
        cached_metadata = self.get_cached_metadata()

        # Check if update is necessary
        cache_modified_time = cached_metadata.get("modified_time", 0)
        from .file_sequence import FileSequence

        if isinstance(self, FileSequence):
            modified_time = self.file_info.modified_time
        else:
            modified_time = os.path.getmtime(self.path)

        return cache_modified_time < modified_time

    def load_cached_metadata(self):
        """Load cached metadata and put in _data_collection (as attributes)"""

        if self.is_cache_invalid():
            self.update_cached_metadata()

        cached_metadata = self.get_cached_metadata()
        # Update _data_collection
        for key, value in cached_metadata.items():
            self.add(key, transform_dict_to_data_containers(value))
            self.cached_attributes.add(key)

        if "valid_loading" in self._data_collection:
            if self.valid_loading is False:
                del self._data_collection["valid_loading"]

        return cached_metadata

    def update_cached_metadata(self):
        """Update cached metadata with instance's fields listed in cached_attributes"""

        cached_metadata = self.get_cached_metadata()
        for key in self.cached_attributes:
            try:
                cached_metadata[key] = transform_data_containers_to_dict(getattr(self, key))
            except AttributeError:
                pass

        self.update_global_cached_metadata(self.unique_identifier)

    def set_cached_metadata_entry(self, key, value):
        cached_metadata = self.get_cached_metadata()
        cached_metadata[key] = transform_data_containers_to_dict(value)
        self.add(key, value)
        self.cached_attributes.add(key)
        self.update_global_cached_metadata(self.unique_identifier)

    def save_field_to_cache(self, key):
        cached_metadata = self.get_cached_metadata()
        cached_metadata[key] = transform_data_containers_to_dict(getattr(self, key))
        self.cached_attributes.add(key)
        self.update_global_cached_metadata(self.unique_identifier)

    @property
    def global_cached_metadata(self) -> BTree:
        return self.get_global_cached_metadata()

    @staticmethod
    def get_global_cached_metadata() -> BTree:
        if CachedMetadata._global_cached_metadata is None:
            CachedMetadata._init_cached_metadata()

        return CachedMetadata._global_cached_metadata

    @classmethod
    def update_global_cached_metadata(cls, unique_identifier=None):
        """Update cached metadata dictionary"""

        if cls._global_cached_metadata is None:
            cls._init_cached_metadata()

        if unique_identifier is not None:
            # Indicate to ZODB that dictionnay has been updated
            cls._global_cached_metadata[unique_identifier] = cls._global_cached_metadata[unique_identifier]

        cls._schedule_commit()
        cls._scheduler.run(blocking=False)

    @classmethod
    def _init_cached_metadata(cls, initial_path="."):
        logger.debug("Loading cached metadata")

        path = get_config_path("cached_metadata_filename", initial_path=initial_path)
        db_file_exists = os.path.exists(path)
        cls._storage = cls._get_zodb_file_storage(path)
        db = ZODB.DB(cls._storage)
        connection = db.open(cls._transaction_manager)
        root = connection.root()

        if "metadata" not in root:
            root["metadata"] = BTree()

        cls._global_cached_metadata = root["metadata"]

        if not db_file_exists:
            cls._populate_cached_metadata_from_yaml(initial_path=initial_path)

    @classmethod
    def clear_cache(cls, exclude=[]):
        if isinstance(exclude, str):
            exclude = [exclude]
        for _file, _meta in cls.get_global_cached_metadata().items():
            keys = [k for k in _meta if k not in exclude + ["modified_time"]]
            for k in keys:
                del _meta[k]
        cls._commit()
        cls.close_cached_metadata()

    @classmethod
    def close_cached_metadata(cls):
        if cls._storage is None:
            return

        cls._cancel_scheduled_commit()
        cls._commit()
        try:
            cls._write_cached_metadata_to_yaml(initial_path=".")
        finally:
            cls._storage.close()
            cls._storage = None
            cls._global_cached_metadata = None
            logger.debug("Closed cached metadata")

    @classmethod
    def _get_zodb_file_storage(cls, path: str) -> ZODB.FileStorage.FileStorage:
        for i in range(cached_metadata_polling_tries):
            try:
                return ZODB.FileStorage.FileStorage(path)
            except LockError:
                logger.debug(f"Could not open cached metadata at {path} ({i + 1} attempts)")
            time.sleep(cached_metadata_polling_interval)

            # import signal
            # import subprocess
            #
            # p = subprocess.Popen(f"lsof {path}", shell=True, stdout=subprocess.PIPE)
            # p.wait()
            # pids = p.stdout.read().decode()
            # pids = pids.split('\n')[1:]
            # pids = [p for p in pids if p != '']
            # for pid in pids[1:]:
            #     pid = pid.split()[1]
            #     os.kill(int(pid), signal.SIGTERM)
        raise LockError(f"Could not open {path}")

    @classmethod
    def _commit(cls):
        """Update cached metadata database"""

        if cls._global_cached_metadata is None:
            return

        logger.debug("Committing cached metadata")
        cls._transaction_manager.commit()
        cls._scheduled_commit = None

    @classmethod
    def _schedule_commit(cls):
        """Schedule later update of metadata database"""

        if cls._scheduled_commit is not None:
            return

        cls._scheduled_commit = cls._scheduler.enter(
            cached_metadata_save_every,
            1,
            cls._commit,
        )

    @classmethod
    def _cancel_scheduled_commit(cls):
        """Cancel scheduled commit"""

        if cls._scheduled_commit is not None:
            cls._scheduler.cancel(cls._scheduled_commit)
            cls._scheduled_commit = None

    cached_property = cached_property
    cached_loadable = cached_loadable

    @classmethod
    def _populate_cached_metadata_from_yaml(cls, initial_path="."):
        """Populate cached metadata from YAML file"""

        metadata_all_files = get_config("cached_metadata_yaml_filename", initial_path=initial_path)
        if metadata_all_files == {}:
            return

        logger.info("Populating cached metadata from YAML file. YAML file will no longer be updated!")
        for unique_identifier, metadata in metadata_all_files.items():
            cls._global_cached_metadata[unique_identifier] = metadata

        cls.update_global_cached_metadata()

    @classmethod
    def _write_cached_metadata_to_yaml(cls, initial_path="."):
        """Write cached metadata to YAML file"""

        logger.info("Writing cached metadata to YAML file")
        metadata_all_files = {}

        for unique_identifier, metadata in cls._global_cached_metadata.items():
            metadata_all_files[unique_identifier] = metadata

        logger.debug(metadata_all_files)
        set_config("cached_metadata_yaml_filename", metadata_all_files, initial_path=initial_path)


atexit.register(CachedMetadata.close_cached_metadata)
