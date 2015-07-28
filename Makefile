OS = $(shell uname -s)
ARCH =  $(shell uname -m)

.PHONY: default
default: dev

.PHONY: deps
deps:
	curl -L https://github.com/docker/compose/releases/download/1.3.2/docker-compose-${OS}-${ARCH} > /usr/local/bin/docker-compose
	chmod +x /usr/local/bin/docker-compose
	pip install -r requirements.txt

.PHONY: clean
clean:
	docker-compose kill
	docker-compose rm -f

.PHONY: migrate
migrate:
	docker-compose run --rm web pypy3 migrations.py

.PHONY: dev
dev: clean
	docker-compose build
	docker-compose up

.PHONY: run
run:
	docker-compose up -d

.PHONY: lint
lint:
	-@pep8 $(wildcard **/*.py);  \
	pylint $(wildcard **/*.py)
