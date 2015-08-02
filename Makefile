OS = $(shell uname -s)
ARCH =  $(shell uname -m)

.PHONY: default
default: build

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
migrate: clean
	docker-compose run --rm web pypy3 migrations.py

.PHONY: build
build: clean
	docker-compose build

.PHONY: dev
dev: clean
	docker-compose up

.PHONY: run
run:
	docker-compose up -d
