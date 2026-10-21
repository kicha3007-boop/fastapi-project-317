#!/usr/bin/env bash

curl -LsSf https://astral.sh/uv/install.sh | sh
. "$HOME/.local/bin/env"
make install && make build-css && make migrate
