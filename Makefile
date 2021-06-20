black:
	black clumper tests setup.py --check

flake:
	flake8 clumper tests setup.py

test:
	pytest

interrogate:
	interrogate -vv --ignore-semiprivate --ignore-private --ignore-magic --fail-under=80 clumper
	interrogate -vv --ignore-semiprivate --ignore-private --ignore-magic --fail-under=80 tests

check: black flake test interrogate

install:
	pip install rich
	python -m pip install -e .

install-dev: install
	python -m pip install -e ".[dev]"
	pre-commit install

install-test: install
	python -m pip install -e ".[test]"
	python -m pip install -e ".[all]"

pypi:
	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*

clean:
	rm -rf **/.ipynb_checkpoints **/.pytest_cache **/__pycache__ **/**/__pycache__ .ipynb_checkpoints .pytest_cache
