#!/bin/bash
# Change to the parent directory of the script
cd "$(dirname "$0")"

source .venv-labelmaker/bin/activate
# By default, a file named gunicorn.conf.py will be read from the same directory where gunicorn is being run.
gunicorn  labelmaker:app
