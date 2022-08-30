#!/bin/bash
python -m pip install --upgrade pip setuptools virtualenv
python -m virtualenv venv
source ./venv/bin/activate
pip install -r development.txt
pip freeze > requirements.txt