#!/usr/bin/env bash
set -eu -o pipefail

cd "$(dirname "$0")/../../.."

django-admin collectstatic --no-input
django-admin migrate
gunicorn -w 10 portscanner.config.wsgi:application --bind 0.0.0.0:8000
