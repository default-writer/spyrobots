#!/bin/bash
python -m pip install --upgrade pip setuptools virtualenv
python -m virtualenv venv
source ./venv/bin/activate
python -m pip install -r dev_requirements.txt