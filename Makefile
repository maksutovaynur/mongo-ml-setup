SHELL                := /bin/bash
DOCKER_COMPOSE_URL   := $(shell echo "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(shell uname -s)-$(shell uname -m)")
LSB_RELEASE          := $(shell lsb_release -cs)

_install-docker:
	@sudo apt-get remove docker docker-engine docker.io containerd runc
	@sudo apt-get update
	@sudo apt-get install apt-transport-https ca-certificates curl gnupg lsb-release
	@curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
	@echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu ${LSB_RELEASE} stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
	@sudo apt-get update
	@sudo apt-get install docker-ce docker-ce-cli containerd.io

_install-docker-compose:
	@echo "Docker-compose url: ${DOCKER_COMPOSE_URL}"
	@sudo curl -L ${DOCKER_COMPOSE_URL} -o /usr/local/bin/docker-compose
	@sudo chmod +x /usr/local/bin/docker-compose

_add-docker-group:
	@sudo usermod -aG docker ${USER}
	@echo "Now please relogin your user before use docker"

_test-docker:
	@sudo docker run hello-world

install-docker: | _install-docker _install-docker-compose _test-docker _add-docker-group

_install-requirements-py:
	@pip install -r requirements.txt

up:
	@docker-compose up -d

down:
	@docker-compose down

example-populate: _install-requirements-py up
	@python example.py

example-flush: up
	@docker exec -it ml-mongo mongo my_database --eval "db.iris.remove({})"

example-browse: up
	@xdg-open http://localhost:9081

example-shell: up
	@docker exec -it ml-mongo mongo
