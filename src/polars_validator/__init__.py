import functools
from collections.abc import Callable
from typing import Generic, ParamSpec, TypeVar

import polars as pl

R = TypeVar("R")
P = ParamSpec("P")


T = TypeVar("T")


def convert_schema_to_polars(schema: type) -> pl.Schema:
    annotations = schema.__annotations__
    converted = {
        name: annotation
        if issubclass(annotation, pl.DataType)
        else pl.DataType.from_python(annotation)
        for name, annotation in annotations.items()
    }
    return pl.Schema(converted)


class DataFrame(pl.DataFrame, Generic[T]):
    def __init__(self, data: pl.DataFrame, schema: type[T]) -> None:
        super().__init__(data)
        self._schema: type[T] = schema
        self.validation_schema: pl.Schema = convert_schema_to_polars(schema)

    def validate(self) -> bool:
        return self.schema == self.validation_schema


def validate_schema(
    schema: type[T],
) -> Callable[[Callable[P, pl.DataFrame]], Callable[P, DataFrame[T]]]:
    def inner(func: Callable[P, pl.DataFrame]) -> Callable[P, DataFrame[T]]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> DataFrame[T]:
            df = func(*args, **kwargs)

            df_ = DataFrame(df, schema)

            if not df_.validate():
                raise ValueError("Schema validation failed")

            return df_

        return wrapper

    return inner
