install:
	pip install --upgrade pip setuptools &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv test_hello.py

format:
	black */*.py

lint:
	pylint --disable=R,C,E1101,W0613 scripts/etl_program.py

all: install lint format