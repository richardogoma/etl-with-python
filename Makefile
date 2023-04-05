install:
	pip install --upgrade pip setuptools &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv test_etl_program.py

format:
	black *.py

lint:
	pylint --disable=R,C,E1101,W0613 etl_program.py

all: install lint format test 