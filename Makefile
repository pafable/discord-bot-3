APP ?= db3
DOCKER ?= docker
PIP ?= $(PYTHON) -m pip
PYTHON ?= python
TAG ?= $(APP):$(VERSION)
VERSION ?= 0.0.1

.PHONY: build deps run which

build:
	$(DOCKER) build . -t $(TAG) --platform linux/amd64 -f Dockerfile

deps:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

deps-dev:
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements-dev.txt

lint: deps
	$(PYTHON) -m pylint --fail-under=8 discord-bot-3

run: deps
	$(PYTHON) discord-bot-3/main.py

run-con: build
	$(DOCKER) run --name discord_bot_3 --env DISCORD_ID=$(DISCORD_ID) --env DISCORD_TOKEN=$(DISCORD_TOKEN) --env AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) --env AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) $(TAG)

which:
	which $(PYTHON)
	$(PYTHON) --version
