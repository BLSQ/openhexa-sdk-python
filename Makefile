.DEFAULT_GOAL := help

.PHONY: help l lint install-editable

help:  ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

lint:  ## Run linting (pre-commit) on all files
	@echo "Executing lint in backend code (pre-commit)"
	pre-commit run --show-diff-on-failure --color=always --all-files

l: lint

install-editable:  ## Install the SDK in editable mode with dev dependencies
	@echo "Installing the SDK in editable mode"
	pip install -e ".[dev]"
