.PHONY: docs test

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    BREWPATH = $(shell brew --prefix)
    PYICU_LD = -L${BREWPATH}/opt/icu4c/lib
    PYICU_CPP = -I${BREWPATH}/opt/icu4c/include
else
    PYICU_LD =
    PYICU_CPP =
endif

help:
	@echo "  env         install all production dependencies"
	@echo "  dev         install all dev and production dependencies (virtualenv is assumed)"
	@echo "  clean       remove unwanted stuff"
	@echo "  lint        check style with flake8"
	@echo "  test        run tests"
	@echo "  build       generate source and wheel dist files"
	@echo "  upload      generate source and wheel dist files and upload them"

env:
	pip install -Ur requirements.txt

dev: env
	pip install -Ur requirements.testing.txt
	@echo "on OS X use homebrew to install icu4c"
	LDFLAGS=${PYICU_LD} CPPFLAGS=${PYICU_CPP} \
    pip install -U pyicu
	pyenv install -s 2.7.11
	pyenv install -s 3.5.2
	pyenv install -s 2.6.9
	pyenv install -s pypy-5.3
	pyenv local 2.7.11 3.5.2 2.6.9 pypy-5.3

info:
	@python --version
	@pyenv --version
	@pip --version

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

tox: clean
	tox

coverage: clean
	@coverage run --source=parsedatetime setup.py test
	@coverage html
	@coverage report

ci: tox coverage
	CODECOV_TOKEN=`cat .codecov-token` codecov

build: clean
	python setup.py check
	python setup.py sdist
	python setup.py bdist_wheel

upload: clean
	python setup.py sdist upload
	python setup.py bdist_wheel upload
