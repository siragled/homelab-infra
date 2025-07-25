.PHONY: help lint test install converge clean

# Default target
help: ## Display this help message
	@echo "Homelab Infrastructure Automation Platform"
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install Ansible dependencies
	@echo "Installing Ansible dependencies..."
	ansible-galaxy install -r requirements.yml --force
	ansible-galaxy collection install -r requirements.yml --force

lint: ## Run linting checks
	@echo "Running linting checks..."
	ansible-lint
	yamllint .

test: ## Run molecule tests
	@echo "Running molecule tests..."
	molecule test

converge: ## Run molecule converge (deploy without destroy)
	@echo "Running molecule converge..."
	molecule converge

clean: ## Clean up cache and temporary files
	@echo "Cleaning up..."
	rm -rf .cache/
	rm -rf .molecule/
	find . -name "*.retry" -delete

site: ## Run the main site.yml playbook
	ansible-playbook plays/99_site.yml

pxe: ## Deploy PXE infrastructure
	ansible-playbook plays/01_pxe.yml

hypervisor: ## Setup hypervisor
	ansible-playbook plays/02_hypervisor.yml

k3s: ## Deploy K3s cluster
	ansible-playbook plays/04_k3s.yml

monitoring: ## Deploy observability stack
	ansible-playbook plays/05_observability.yml
