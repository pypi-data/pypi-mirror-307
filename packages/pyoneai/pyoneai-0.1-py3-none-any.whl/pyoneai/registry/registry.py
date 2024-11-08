__all__ = (
    "Registry",
    "FileRegistry",
)
from abc import ABC, abstractmethod
from pathlib import Path
from types import MappingProxyType
from typing import Any, Callable


def _make_immutable(d):
    """
    Recursively makes dictionaries read-only using MappingProxyType.

    Parameters:
    -----------
    d : dict
        The dictionary to make immutable recursively.

    Returns:
    -------
    dict
        A read-only version of the dictionary.
    """
    if isinstance(d, dict):
        return MappingProxyType({k: _make_immutable(v) for k, v in d.items()})
    return d


class Registry(ABC):

    def __getitem__(self, key: str) -> Any:
        if isinstance(res := self._get(key), dict):
            return _make_immutable(res)
        return res

    def reset(self) -> None:
        self.connect()

    @abstractmethod
    def _get(self, key: str) -> Any:
        raise NotImplementedError

    @abstractmethod
    def update_prediction(
        self,
        entity: str,
        metric: str,
        model: Any = None,
        path: str | None = None,
        model_args: list | None = None,
        model_kwargs: dict | None = None,
        historical_period: str | None = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_prediction(
        self,
        entity: str,
        metric: str,
        model: Any = None,
        path: str | None = None,
        model_args: list | None = None,
        model_kwargs: dict | None = None,
        historical_period: str | None = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_accessor(
        self,
        entity: str,
        metric: str,
        model: Any = None,
        model_args: list | None = None,
        model_kwargs: dict | None = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_accessor(
        self,
        entity: str,
        metric: str,
        model: Any,
        model_args: list | None = None,
        model_kwargs: dict | None = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def update_derived(
        self,
        entity: str,
        metric: str,
        model: Any,
        model_args: list | None = None,
        model_kwargs: dict | None = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def add_derived(
        self,
        entity: str,
        metric: str,
        model: Any,
        model_args: list | None = None,
        model_kwargs: dict | None = None,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def save(self) -> None:
        raise NotImplementedError


class FileRegistry(Registry):
    _JSON_EXTENSIONS = (".json",)
    _YAML_EXTENSIONS = (".yaml", ".yml")
    _SUPPORTED_EXTENSIONS = _JSON_EXTENSIONS + _YAML_EXTENSIONS

    def __init__(self, path: str) -> None:
        self.path = Path(path).expanduser()
        if not self.path.exists():
            raise FileNotFoundError(
                f"The registry file {self.path} does not exist"
            )
        if self.path.suffix not in self._SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"The registry file {self.path} has an unsupported extension. "
                "The supported extensions are: "
                f"{', '.join(self._SUPPORTED_EXTENSIONS)}"
            )
        self.registry = self._load_registry()

    @property
    def _read_file(self) -> Callable:
        match self.path.suffix:
            case x if x in self._JSON_EXTENSIONS:
                import json

                return json.load
            case x if x in self._YAML_EXTENSIONS:
                import yaml

                return yaml.safe_load

    @property
    def _write_file(self) -> Callable:
        match self.path.suffix:
            case x if x in self._JSON_EXTENSIONS:
                import json

                return json.dump
            case x if x in self._YAML_EXTENSIONS:
                import yaml

                return yaml.dump

    def _load_registry(self) -> dict:
        with open(self.path, "r") as file:
            registry = self._read_file(file)
        return registry

    def connect(self) -> None:
        self.registry = self._load_registry()

    def reset(self) -> None:
        self.registry = self._load_registry()

    def save(self) -> None:
        with open(self.path, "wt") as file:
            self._write_file(self.registry, file)

    def update_prediction(
        self,
        entity: str,
        metric: str,
        model: Any = None,
        path: str | None = None,
        model_args: list | None = None,
        model_kwargs: dict | None = None,
        historical_period: str | None = None,
    ) -> None:
        if model:
            self.registry[entity][metric]["prediction"]["class"] = model
        if path:
            self.registry[entity][metric]["prediction"]["path"] = path
        if historical_period:
            self.registry[entity][metric]["prediction"][
                "historical_period"
            ] = historical_period
        if model_args:
            self.registry[entity][metric]["prediction"]["args"] = (
                model_args or []
            )
        if model_kwargs:
            self.registry[entity][metric]["prediction"]["kwargs"] = (
                model_kwargs or {}
            )

    def add_prediction(
        self,
        entity: str,
        metric: str,
        model: Any,
        path: str,
        model_args: list | None = None,
        model_kwargs: dict | None = None,
        historical_period: str | None = None,
    ) -> None:
        if metric not in self.registry[entity]:
            self.registry[entity][metric] = {}
        if "prediction" in self.registry[entity][metric]:
            raise ValueError(
                f"Prediction configuration for {metric} already exists "
                "in the registry. If you want to update it, "
                "please use `update_prediction` method instead."
            )
        self.registry[entity][metric]["prediction"] = {
            "class": model,
            "path": path,
            "args": model_args or [],
            "kwargs": model_kwargs or {},
            "historical_period": historical_period,
        }

    def update_accessor(
        self,
        entity: str,
        metric: str,
        model: Any = None,
        model_args: list | None = None,
        model_kwargs: dict | None = None,
    ) -> None:
        if model:
            self.registry[entity][metric]["accessor"]["class"] = model
        if model_args:
            self.registry[entity][metric]["accessor"]["args"] = (
                model_args or []
            )
        if model_kwargs:
            self.registry[entity][metric]["accessor"]["kwargs"] = (
                model_kwargs or {}
            )

    def add_accessor(
        self,
        entity: str,
        metric: str,
        model: Any,
        model_args: list | None = None,
        model_kwargs: dict | None = None,
    ) -> None:
        if metric not in self.registry[entity]:
            self.registry[entity][metric] = {}
        if "accessor" in self.registry[entity][metric]:
            raise ValueError(
                f"Accessor configuration for {metric} already exists "
                "in the registry. If you want to update it, "
                "please use `update_accessor` method instead."
            )
        self.registry[entity][metric]["accessor"] = {
            "class": model,
            "args": model_args or [],
            "kwargs": model_kwargs or {},
        }

    def update_derived(
        self,
        entity: str,
        metric: str,
        model: Any = None,
        model_args: list | None = None,
        model_kwargs: dict | None = None,
    ) -> None:
        if model:
            self.registry[entity][metric]["derived"]["class"] = model
        if model_args:
            self.registry[entity][metric]["derived"]["args"] = model_args or []
        if model_kwargs:
            self.registry[entity][metric]["derived"]["kwargs"] = (
                model_kwargs or {}
            )

    def add_derived(
        self,
        entity: str,
        metric: str,
        model: Any,
        model_args: list | None = None,
        model_kwargs: dict | None = None,
    ) -> None:
        if metric not in self.registry[entity]:
            self.registry[entity][metric] = {}
        if "derived" in self.registry[entity][metric]:
            raise ValueError(
                f"Derived configuration for {metric} already exists "
                "in the registry. If you want to update it, "
                "please use `update_derived` method instead."
            )
        self.registry[entity][metric]["derived"] = {
            "class": model,
            "args": model_args or [],
            "kwargs": model_kwargs or {},
        }

    def _get(self, key: str) -> Any:
        return self.registry[key]
