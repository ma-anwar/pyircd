
.DEFAULT_GOAL:=help

# Check if poetry is available when we run
POETRY := $(shell command -v poetry 2> /dev/null)

.PHONY: install
install: ## Set up repo and commit hooks
	@$(POETRY) install
	@$(POETRY) run pre-commit install


# Adapted from https://www.thapaliya.com/en/writings/well-documented-makefiles/
.PHONY: help
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
