#!/usr/bin/env bash
#
# Bootstrap local dev environment.
#
set -eu -o pipefail

# TODO: Add checks for direnv, pyenv & nmap
direnv allow

cd "$(dirname "$0")/.."

# Parse .python-version
venv=$(cat .python-version)
version=${venv/[a-zA-Z0-9\-]*\-/}

PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install -s ${version}
pyenv virtualenv -f ${version} ${venv}

pip install -r dev-requirements.txt || echo "!! Cannot install dev requirements !!"

echo "Bootstrap complete"

