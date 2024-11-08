#!/bin/bash -e

rm -rf dist/
source ./venv/bin/activate
python -m build
twine upload dist/*
