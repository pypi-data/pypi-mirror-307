import importlib
import inspect
import pkgutil
import pprint
import sys

from ..utils import logging

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points

print = logging.invalidPrint
logger = logging.getLogger()


PLUGINS_GROUP_NAME = "solidipes.plugins"


def _get_subclasses_from_plugins(
    plugins_package_names: "PluginsPackageNames",
    subpackage_name: str,
    BaseClass: type,
) -> set[type]:
    """Get all subclasses of a base class in all plugins"""

    subclasses = set()

    for package_name in plugins_package_names:
        try:
            package = importlib.import_module(f"{package_name}.{subpackage_name}")
        except ModuleNotFoundError:
            continue

        subclasses.update(get_subclasses_from_package(package, BaseClass))

    return subclasses


def get_subclasses_from_package(
    package,
    BaseClass: type,
) -> set[type]:
    """Get all subclasses of a base class in a package"""

    module_names = [module.name for module in pkgutil.iter_modules(package.__path__) if module.ispkg is False]
    modules = [importlib.import_module(f"{package.__name__}.{module_name}") for module_name in module_names]

    subclasses_set = set()
    for module in modules:
        subclasses_set.update(_get_subclasses_from_module(module, BaseClass))

    return subclasses_set


def _get_subclasses_from_module(module, BaseClass: type) -> set[type]:
    subclasses = {
        obj
        for name, obj in inspect.getmembers(module)
        if inspect.isclass(obj) and issubclass(obj, BaseClass) and obj != BaseClass
    }

    if len(subclasses) == 0:
        logger.debug(f"Could not find subclass of {BaseClass.__name__} in module {module}")

    return subclasses


def _get_list_ordered_by_inheritance(object_set: set) -> list:
    """Get a list of objects ordered by their inheritance depth. Children first."""

    def get_inheritance_depth(cls):
        return -len(inspect.getmro(cls))

    return sorted(object_set, key=get_inheritance_depth)


class LazyList:
    """Lazily evaluated list"""

    def __init__(self):
        self._list = []

    def _populate_list(self):
        raise NotImplementedError

    def reset(self):
        self._list = []

    @property
    def list(self):
        if not self._list:
            self._populate_list()

        return self._list

    def __iter__(self):
        return iter(self.list)

    def __getitem__(self, item):
        return self.list[item]

    def __len__(self):
        return len(self.list)

    def __repr__(self):
        return pprint.pformat(self.list)


class PluginsPackageNames(LazyList):
    """Lazily evaluated list of plugins package names"""

    def _populate_list(self):
        plugins = entry_points(group=PLUGINS_GROUP_NAME)
        self._list = [p.value for p in plugins]


class ClassList(LazyList):
    """Lazily evaluated list of classes"""

    def __init__(self):
        super().__init__()

        #: List of subclasses, ordered by priority
        self._list = []

        #: Dictionary of subclasses, keyed by class name.
        #: Classes further down the inheritance chain take precedence
        self._dict = {}

        #: Dictionary of subclasses, keyed by full class path (__module__ + __qualname__)
        self._full_dict = {}

    def _populate_dict(self):
        for cls in self.list:
            class_name = cls.__name__
            self._dict[class_name] = cls

    def _populate_full_dict(self):
        for cls in self.list:
            class_path = f"{cls.__module__}.{cls.__qualname__}"
            self._full_dict[class_path] = cls

    def reset(self):
        self._list = []
        self._dict = {}
        self._full_dict = {}

    def as_dict(self) -> dict[str, type]:
        if not self._dict:
            self._populate_dict()

        return self._dict

    def as_full_dict(self) -> dict[str, type]:
        if not self._full_dict:
            self._populate_full_dict()

        return self._full_dict


class LoaderList(ClassList):
    """Lazily evaluated list of loaders"""

    def __init__(self, plugins_package_names: PluginsPackageNames):
        super().__init__()
        self._plugins_package_names = plugins_package_names

    def _populate_list(self):
        from solidipes_core_plugin.loaders.binary import Binary

        from ..loaders.data_container import DataContainer
        from ..loaders.file import File
        from ..loaders.file_sequence import FileSequence
        from ..loaders.sequence import Sequence

        # Note: the first matching type is used
        loaders_set = _get_subclasses_from_plugins(self._plugins_package_names, "loaders", DataContainer)
        loaders_set = loaders_set - {Binary, File, FileSequence, Sequence}

        self._list = _get_list_ordered_by_inheritance(loaders_set)
        self._list.append(Binary)  # Needs to stay at the end


class ViewerList(ClassList):
    """Lazily evaluated list of viewers"""

    def __init__(self, plugins_package_names: PluginsPackageNames):
        super().__init__()
        self._plugins_package_names = plugins_package_names

    def _populate_list(self):
        from ..viewers.viewer import Viewer

        viewers_set = _get_subclasses_from_plugins(self._plugins_package_names, "viewers", Viewer)
        self._list = _get_list_ordered_by_inheritance(viewers_set)


plugins_package_names = PluginsPackageNames()
loader_list = LoaderList(plugins_package_names)
viewer_list = ViewerList(plugins_package_names)
