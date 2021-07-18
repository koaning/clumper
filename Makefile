black:
	black clumper tests setup.py --check

flake:
	flake8 clumper tests setup.py

test:
	pytest

interrogate:
<<<<<<< HEAD
	interrogate -vv --ignore-semiprivate --ignore-private --ignore-magic --fail-under=80 clumper
	interrogate -vv --ignore-semiprivate --ignore-private --ignore-magic --fail-under=80 tests
=======
	interrogate -vv --ignore-nested-functions --ignore-semiprivate --ignore-private --ignore-magic --ignore-module --ignore-init-method --fail-under 100 tests
	interrogate -vv --ignore-nested-functions --ignore-semiprivate --ignore-private --ignore-magic --ignore-module --ignore-init-method --fail-under 100 clumper
>>>>>>> df12a70bd91ed8713c7960f9b074e9675c5479b2

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
