from collections.abc import Mapping
from typing import Generic, TypeVar

import polars as pl

__all__ = [
    "DataFrame",
]


S = TypeVar("S", bound=Mapping)
H = TypeVar("H", int, None, default=None)


class DataFrame(pl.DataFrame, Generic[S, H]):
    """No-op class to make Polars DataFrames generics."""

    def __init__(
        self,
        data: pl.DataFrame,
        schema: type[S],
        height: H = None,
    ) -> None:
        super().__init__(data)
        self._schema_base: type[S] = schema
        self._schema_height: H = height
        self._validation_schema: pl.Schema = _convert_schema_to_polars(schema)


def _convert_schema_to_polars(schema: type) -> pl.Schema:
    annotations = schema.__annotations__
    converted = {
        name: annotation
        if issubclass(annotation, pl.DataType)
        else pl.DataType.from_python(annotation)
        for name, annotation in annotations.items()
    }
    return pl.Schema(converted)
