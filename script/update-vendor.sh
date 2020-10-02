#!/usr/bin/env bash
#
# Update requirements.txt
#
set -eu -o pipefail

cd "$(dirname "$0")/.."

pip install --no-cache-dir --upgrade -t vendor -r requirements.txt

# fix bin scripts
if [[ -d vendor/bin ]]; then
  find vendor/bin -type f -maxdepth 1 | xargs sed -i '' 's/^#!.*$/#!\/usr\/bin\/env python/'
fi
