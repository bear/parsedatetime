.PHONY: docs test

help:
	@echo "  env         install all production dependencies"
	@echo "  dev         install all dev and production dependencies (virtualenv is assumed)"
	@echo "  clean       remove unwanted stuff"
	@echo "  lint        check style with flake8"
	@echo "  test        run tests"
	@echo "  build       generate source and wheel dist files"
	@echo "  upload      generate source and wheel dist files and upload them"

env:
	pip install -r requirements.txt

dev: env
	pip install -r requirements.testing.txt
	LDFLAGS=-L/usr/local/opt/icu4c/lib CPPFLAGS=-I/usr/local/opt/icu4c/include \
    pip install pyicu

info:
	python --version
	pyenv --version
	pip --version

clean:
	rm -fr build
	rm -fr dist
	find . -name '*.pyc' -exec rm -f {} \;
	find . -name '*.pyo' -exec rm -f {} \;
	find . -name '*~' -exec rm -f {} \;

docs:
	epydoc --html --config epydoc.conf

lint:
	flake8 parsedatetime > violations.flake8.txt

test: lint
	python setup.py test

coverage: clean
	coverage run --source=parsedatetime setup.py test
	coverage html
	coverage report

build: clean
	python setup.py check
	python setup.py sdist
	python setup.py bdist_wheel

upload: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload
