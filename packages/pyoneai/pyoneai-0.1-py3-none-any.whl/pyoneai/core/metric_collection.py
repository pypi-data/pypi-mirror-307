__all__ = ["MetricCollection", "PoolMetricCollection"]

import re
from collections.abc import Collection

from .metric_accessors import (
    DerivedMetricAccessor,
    MetricAccessor,
    MetricAccessors,
    PoolMetricAccessor,
)


class MetricCollection:
    __slots__ = ("_entity", "_data")

    # TODO: Generalize regular expressions.
    _SIMPLE_PATTERN = re.compile(r"^[a-z_]*$")
    _COMPOSITE_PATTERN = tuple(
        re.compile(rf"^[a-z_]*\({'[a-z_ ]*,' * i}[a-z_ ]*\)$")
        for i in range(5)
    )

    def __init__(self, entity) -> None:
        self._entity = entity
        self._data: dict[str, DerivedMetricAccessor | MetricAccessor] = {}

    def __getitem__(
        self, key: str | Collection[str]
    ) -> DerivedMetricAccessor | MetricAccessor | MetricAccessors:
        match key:
            case str():
                if key not in self._data:
                    self._data[key] = self._resolve_name(key)
                return self._data[key]
            case Collection():
                return MetricAccessors(self._entity, key)
            case _:
                raise TypeError("'key' must be a string or other collection")

    def _resolve_name(
        self, name: str
    ) -> DerivedMetricAccessor | MetricAccessor:
        if re.match(self._SIMPLE_PATTERN, name):
            if name not in self._entity.registry:
                raise KeyError(f"'name' is not in the registry: {name}")
            return MetricAccessor(self._entity, name)

        if any(re.match(pattern, name) for pattern in self._COMPOSITE_PATTERN):
            i = name.find("(")
            j = name.find(")")
            var_name = name[:i]
            covar_names = [item.strip() for item in name[i + 1 : j].split(",")]
            if var_name not in self._entity.registry:
                raise KeyError(f"'name' is not in the registry: {var_name}")
            return DerivedMetricAccessor(self._entity, var_name, covar_names)

        raise ValueError(f"'name' has the inappropriate value '{name}'")


class PoolMetricCollection:
    __slots__ = ("_pool",)

    def __init__(self, pool) -> None:
        self._pool = pool

    def __getitem__(self, key: str | Collection[str]) -> PoolMetricAccessor:
        return PoolMetricAccessor(self._pool, key)
