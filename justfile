set quiet := true

default: format lint check

format: (needs "uv")
    uvx ruff format -- src
    uvx ruff check --select=I,RUF022 --fix -- src

lint: (needs "uv")
    uvx ruff check -- src test

check: (needs "bun" "uv")
    echo "=========== mypy ============"
    # `-` will continue execution even if the command fails
    -uvx mypy --strict -- src tests

    echo "\n========== pyright =========="
    bunx pyright -- src tests

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
