#!/bin/sh
set -eu
exec gunicorn --bind "0.0.0.0:${PORT:-4178}" --workers 1 --threads 4 --access-logfile - --error-logfile - api.index:app
