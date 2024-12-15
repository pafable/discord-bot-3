APP ?= discord-bot-3
DOCKER ?= docker
PIP ?= $(PYTHON) -m pip
PIP_INSTALL_FILE ?= requirements
PYTHON ?= python
TAG ?= $(APP):$(VERSION)
VERSION ?= 0.0.1

.PHONY: build deps deps-dev lint run run-con which

build:
	$(DOCKER) build . -t $(TAG) --platform linux/amd64 -f Dockerfile

deps:
	$(PIP) install --upgrade pip
	$(PIP) install -r $(PIP_INSTALL_FILE).txt

deps-dev:
	$(PIP) install --upgrade pip
	$(PIP) install -r $(PIP_INSTALL_FILE)-dev.txt

lint: deps
	$(PYTHON) -m pylint --fail-under=8 $(APP)

run: deps
	$(PYTHON) $(APP)/main.py

run-con: build
	$(DOCKER) run --name $(APP) --env DISCORD_ID=$(DISCORD_ID) --env DISCORD_TOKEN=$(DISCORD_TOKEN) --env AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) --env AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) $(TAG)

which:
	which $(PYTHON)
	$(PYTHON) --version
