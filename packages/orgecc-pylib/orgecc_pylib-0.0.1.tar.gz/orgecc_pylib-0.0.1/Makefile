.PHONY: all version v test t dist d clean c

all: test version

version v:
	git describe --tags ||:
	python -m setuptools_scm

test t:
	echo todo pytest --cov=src/pylibtypes tests/ --cov-report term-missing

dist d: test
	scripts/check-version.sh
	rm -rf dist/
	# SETUPTOOLS_SCM_PRETEND_VERSION=0.0.1
	python -m build && twine upload dist/*

clean c:
	rm -rfv out dist build/bdist.*
