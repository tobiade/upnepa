# Makefile

# Variables
REMOTE_USER ?= tobi
REMOTE_HOST ?= ocean
FRONTEND_REMOTE_PATH ?= /var/www/upnepa-app
LOCAL = local
REMOTE = remote

# Paths
PYTHON_DIR = python
VENV_DIR = $(PYTHON_DIR)/venv
REQUIREMENTS = $(PYTHON_DIR)/requirements.txt
PROJECT_DIR = /Development/upnepa
SCRIPTS_DIR = /home/$(REMOTE_USER)/$(PROJECT_DIR)/scripts

# Services to manage
SERVICES = socket_server main video_feed

# Default target
.PHONY: all
all: help

# Help target
.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  build                Build the React application"
	@echo "  deploy-local         Deploy services locally"
	@echo "  deploy-remote        Deploy services to remote server"
	@echo "  install-local        Install systemd services locally"
	@echo "  install-remote       Install systemd services on remote server"
	@echo "  start                Start all services"
	@echo "  stop                 Stop all services"
	@echo "  restart              Restart all services"
	@echo "  status               Show status of all services"
	@echo ""

# Build React app
.PHONY: build-frontend
build-frontend:
	cd frontend && npm run build

# Deploy frontend remote
.PHONY: deploy-frontend-remote
deploy-frontend-remote:
	scp -r frontend/build/* $(REMOTE_HOST):$(FRONTEND_REMOTE_PATH)

# Deploy Python services to remote server
.PHONY: deploy-services-remote
deploy-services-remote:
	ssh $(REMOTE_HOST) "bash $(SCRIPTS_DIR)/register_service.sh"
	
# Deploy Python services locally
.PHONY: deploy-services-local
deploy-services-local:
	scripts/deploy_pi.sh
	

