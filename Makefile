.PHONY: dev info clean docs lint test

help:
	@echo "  dev         install all dev and production dependencies (virtualenv is assumed)"
	@echo "  clean       remove unwanted stuff"
	@echo "  lint        check style with flake8"
	@echo "  test        run tests"
	@echo "  build       generate source and wheel dist files"
	@echo "  upload      generate source and wheel dist files and upload them"

info:
	@pipenv --version
	@pipenv run python --version

env: info
	pipenv install --dev --python 3.9
	pipenv install black --pre --dev

dev: info
	pipenv install --dev

clean:
	rm -fr build
	rm -fr dist
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' -exec rm -f {} \;

docs:
	pipenv run epydoc --html --config epydoc.conf

lint: clean
	pipenv run flake8 parsedatetime  > violations.txt
	pipenv run mypy parsedatetime   >> violations.txt

test: clean
	pipenv run pytest

coverage: clean
	@pipenv run coverage run --source=parsedatetime setup.py test
	@pipenv run coverage html
	@pipenv run coverage report

check: clean lint
	pipenv run python setup.py check

build: check
	pipenv run python setup.py sdist bdist_wheel

# requires PyPI Twine - brew install pypi-twine
upload: build
	twine upload dist/*
