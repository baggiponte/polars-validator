from typing import TypedDict

import polars as pl

from polars_validator import DataFrame, check_schema


def test_validate_schema():
    class User(TypedDict):
        id: int
        name: str
        email: str

    @check_schema(User)
    def get_users_from_db() -> pl.DataFrame:
        # Simulate database query
        data = [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
        ]
        return pl.DataFrame(data)

    users: DataFrame[User] = get_users_from_db()
