.PHONY: dev info clean docs lint test

help:
	@echo "  dev         install all dev and production dependencies (virtualenv is assumed)"
	@echo "  clean       remove unwanted stuff"
	@echo "  lint        check style with flake8"
	@echo "  test        run tests"
	@echo "  build       generate source and wheel dist files"
	@echo "  upload      generate source and wheel dist files and upload them"

dev:
	pipenv install --dev --python 3.7

info:
	@pipenv --version
	@pipenv run python --version

clean:
	rm -fr build
	rm -fr dist
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' -exec rm -f {} \;

docs:
	pipenv run epydoc --html --config epydoc.conf

lint:
	pipenv run flake8 parsedatetime > violations.flake8.txt

test:
	pipenv run python setup.py test

tox: clean
	pipenv run tox

coverage: clean
	@pipenv run coverage run --source=parsedatetime setup.py test
	@pipenv run coverage html
	@pipenv run coverage report

build: clean
	pipenv run python setup.py check
	pipenv run python setup.py sdist
	pipenv run python setup.py bdist_wheel

upload: clean
	pipenv run python setup.py sdist upload
	pipenv run python setup.py bdist_wheel upload
