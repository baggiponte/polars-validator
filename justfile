set quiet := true

lint: format
    uvx ruff check -- src test

format: (needs "uv")
    uvx ruff format -- src
    uvx ruff check --select=I,RUF022 --fix -- src

lint: (needs "uv")
    uvx ruff check -- src tests

mypy: (needs "uv")
    uvx mypy --strict -- src tests

pyright: (needs "bun")
    bunx pyright src tests

test: (needs "pytest")
    uv run pytest tests

[private]
needs +commands:
    #!/usr/bin/env zsh
    set -euo pipefail
    for cmd in "$@"; do
      if ! command -v $cmd &> /dev/null; then
        echo "$cmd binary not found. Make sure you install it first."
        exit 1
      fi
    done
