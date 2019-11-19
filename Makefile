.PHONY: docs test

UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    BREWPATH = $(shell brew --prefix)
    PYICU_LD = "-L${BREWPATH}/opt/icu4c/lib -L${BREWPATH}/opt/openssl@1.1/lib"
    PYICU_CPP = "-I${BREWPATH}/opt/icu4c/include -I${BREWPATH}/opt/openssl@1.1/include"
	ICU_VER = 58.2
else
    PYICU_LD =
    PYICU_CPP =
	ICU_VER =
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
	pipenv install

dev: env
	@echo "on OS X use homebrew to install icu4c"
	LDFLAGS=${PYICU_LD} CPPFLAGS=${PYICU_CPP} ICU_VERSION=${ICU_VER} \
	pipenv --python 2.7
	pipenv --python 3.7

info:
	@python --version
	@pipenv --version

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

test: lint
	pipenv run python setup.py test

tox: clean
	pipenv run tox

coverage: clean
	@pipenv run coverage run --source=parsedatetime setup.py test
	@pipenv run coverage html
	@pipenv run coverage report

ci: tox coverage
	CODECOV_TOKEN=`cat .codecov-token` pipenv run codecov

build: clean
	pipenv run python setup.py check
	pipenv run python setup.py sdist
	pipenv run python setup.py bdist_wheel

upload: clean
	pipenv run python setup.py sdist upload
	pipenv run python setup.py bdist_wheel upload
