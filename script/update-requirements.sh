#!/usr/bin/env bash
#
# Update requirements.txt
#
set -eu -o pipefail

cd "$(dirname "$0")/.."

pip-compile -q -o requirements.txt --no-emit-index-url requirements.in
pip-compile -q -o dev-requirements.txt --no-emit-index-url dev-requirements.in

