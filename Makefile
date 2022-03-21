PYTHON ?= python3
export PYTHONIOENCODING =? "utf-8"

test:
	+$(MAKE) -C recipes clean
	+$(MAKE) -C recipes

coverage:
	+$(MAKE) -C recipes coverage

develop:
	(which opam || { echo "OPAM not found; please install it"; exit 1; })
	eval $$(opam env); opam install coq-serapi
	$(PYTHON) -m pip install coverage[toml]
	$(PYTHON) -m mypy --install-types alectryon/
	@# Local install; should be ‘pip install -e .[full]’ but see https://github.com/pypa/pip/issues/7953
	$(PYTHON) -c 'import setuptools, site, sys; site.ENABLE_USER_SITE = 1; sys.argv[1:] = ["develop", "--user"]; setuptools.setup()'

.PHONY: dist

dist:
	$(PYTHON) -m build

upload: dist
	$(PYTHON) -m twine upload dist/*

lint-changes:
	etc/lint_changes.py CHANGES.rst

lint:
	vermin --target=3.6- --violations alectryon
	pylint --rcfile=setup.cfg alectryon
	mypy alectryon/
	pyright --project .

FORCE:
recipes/%: FORCE
	+$(MAKE) -C recipes --always-make "$*"
