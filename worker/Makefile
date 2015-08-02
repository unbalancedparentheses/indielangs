.PHONY: default
default: test

.PHONY: lint
lint:
	-@pep8 $(wildcard **/*.py);  \
	pylint $(wildcard **/*.py)

.PHONY: test
test:
	tox
