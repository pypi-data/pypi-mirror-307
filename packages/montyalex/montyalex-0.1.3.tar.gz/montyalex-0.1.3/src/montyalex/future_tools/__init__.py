import importlib
from inspect import isclass, isfunction

from montyalex.typing_tools import Callable, Type, Union, Dict


class MonthlyFeatures:
    _monthly_feature_map = {
        "2024_11": "montyalex.future_tools.by_2024_11_27",
        "2024_12": "montyalex.future_tools.by_2024_12_25",
    }

    def __init__(self, release_date: str):
        self.release_date = release_date
        self.features: Dict[str, Union[Type[object], Callable]] = self.load_month(release_date)

    def load_month(
            self, release_date: str) -> Dict[str, Union[Type[object], Callable]]:
        """Dynamically import module and return a dictionary of classes and functions by name."""
        module_name = self._monthly_feature_map.get(release_date[:7])
        if not module_name:
            return {}

        module = importlib.import_module(module_name)

        features = {
            name: getattr(module, name)
            for name in dir(module)
            if (isclass(getattr(module, name)) or isfunction(getattr(module, name)))
            and getattr(module, name).__module__ == module_name
        }

        return features

    def __getattr__(self, item: str):
        """Allow dynamic access to features as attributes."""
        if item in self.features:
            return self.features[item]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")


    @property
    def exceptions(self) -> Dict[str, Type[BaseException]]:
        """Return only the features that are exceptions."""
        return {
            name: feature
            for name, feature in self.features.items()
            if isclass(feature) and issubclass(feature, BaseException)
        }

    @property
    def functions(self) -> Dict[str, Callable]:
        """Return only the features that are functions."""
        return {
            name: feature
            for name, feature in self.features.items()
            if isfunction(feature)
        }

    @property
    def other_classes(self) -> Dict[str, Type[object]]:
        """Return only the features that are classes but not exceptions."""
        return {
            name: feature
            for name, feature in self.features.items()
            if isclass(feature) and not issubclass(feature, BaseException)
        }

    @property
    def matching_features(self, keyword: str) -> Dict[str, Union[Type[object], Callable]]:
        """Return features with a specific keyword in their name (case-insensitive)."""
        return {
            name: feature
            for name, feature in self.features.items()
            if keyword.lower() in name.lower()
        }

__november24__ = MonthlyFeatures("2024_11_27")
__december24__ = MonthlyFeatures("2024_12_25")
__version__ = 'v.1.0.0'


__all__ = [
    "__november24__",
    "__december24__",
    "__version__"]