& python -m pip install --upgrade pip setuptools virtualenv
& python -m virtualenv .venv
& ./.venv/Scripts/activate
& pip install -r development.txt
& pip freeze > requirements.txt