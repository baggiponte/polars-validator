import functools
from collections.abc import Callable, Mapping
from typing import ParamSpec, TypeVar

import polars as pl

from polars_validator.dataframe import DataFrame

S = TypeVar("S", bound=Mapping)
H = TypeVar("H", int, None, default=None)

R = TypeVar("R")
P = ParamSpec("P")

__all__ = [
    "check_schema",
]


def check_schema(
    schema: type[S],
) -> Callable[[Callable[P, pl.DataFrame]], Callable[P, DataFrame[S]]]:
    def inner(func: Callable[P, pl.DataFrame]) -> Callable[P, DataFrame[S]]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> DataFrame[S]:
            df = func(*args, **kwargs)

            df_ = DataFrame(df, schema)

            if not df_.validate():
                raise ValueError("Schema validation failed")

            return df_

        return wrapper

    return inner
