from ..utils import solidipes_logging as logging
from .data_container import DataContainer

logger = logging.getLogger()


class Sequence(DataContainer):
    """Sequence of any subclass of DataContainer"""

    def __init__(self, _selected_element=0, **kwargs):
        self._elements = {}
        self._selected_element = _selected_element
        super().__init__(**kwargs)

    @property
    def _current_element(self):
        element = self._elements.get(self._selected_element, None)

        # Load element if not already loaded
        if element is None:
            element = self._load_element(self._selected_element)
            self._elements[self._selected_element] = element

        return element

    @property
    def sequence_type(self):
        return type(self._load_element(0))

    def select_element(self, n: int):
        self._selected_element = n

    def _load_element(self, n: int):
        """Must raise KeyError if element does not exist

        Override this method in subclasses.
        """

        raise NotImplementedError

    def __getattr__(self, key):
        logger.debug(f"__getattr__({type(self)}, {key})")
        try:
            return self.get(key)
        except KeyError:
            pass

        return getattr(self._current_element, key)

    @property
    def default_viewer(self):
        """Return the default viewer of the current element"""

        if len(self.compatible_viewers) > 0:
            return self.compatible_viewers[0]

        return getattr(self._current_element, "default_viewer", None)
