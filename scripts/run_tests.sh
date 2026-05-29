#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

export PYTEST_DISABLE_PLUGIN_AUTOLOAD=1
python -m pytest -q
