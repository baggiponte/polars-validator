# Polars Validator

Make your Polars DataFrames generics!

## Installation

```bash
uv add git+https://github.com/baggiponte/polars-validator
```

## Usage

```python
from typing import TypedDict

import polars as pl
from polars_validator import validate_schema, DataFrame

class User(TypedDict):
        id: int
        name: str
        email: str

@validate_schema(User)
def get_users_from_db() -> pl.DataFrame:
    # Simulate database query
    data = [
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
    ]
    return pl.DataFrame(data)

users: DataFrame[User] = get_users_from_db()
```

## Development

### Run tests

It's faster with [just](https://just.systems).
