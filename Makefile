# Enable BuildKit for docker builds
export DOCKER_BUILDKIT=1

# Variables for Docker build
DOCKER_REGISTRY=ghcr.io
GRADLE_PROPS_FILE=$(HOME)/.gradle/gradle.properties
DOCKER_REGISTRY_USERNAME=$(shell echo $${DOCKER_REGISTRY_USERNAME:-$(shell grep '^gpr\.user=' $(GRADLE_PROPS_FILE) 2>/dev/null | cut -d'=' -f2 || echo "")})
DOCKER_REGISTRY_TOKEN=$(shell echo $${DOCKER_REGISTRY_TOKEN:-$(shell grep '^gpr\.token=' $(GRADLE_PROPS_FILE) 2>/dev/null | cut -d'=' -f2 || echo "")})
IMAGE_NAME=ck-graph-mcp

.PHONY: help check-credentials setup-gradle-props build-and-deploy-ckqa build-and-deploy-prod build-and-deploy-gcp-fk-ckqa build-and-deploy-gcp-demo build-and-deploy-flipkart deploy-ckqa deploy-prod deploy-gcp-fk-ckqa deploy-gcp-demo deploy-flipkart build-and-deploy-local dockerise-local deploy-common help-detailed verify-context verify-ckqa-context verify-prod-context verify-gcp-fk-ckqa-context verify-gcp-demo-context verify-flipkart-context verify-local-context create-registry-secret build-docker-image build-cleartrip build-flipkart run-local run-remote test-remote install-deps generate-config docker-up docker-down docker-logs docker-test

# Default target when just 'make' is run
help:
	@echo "ck-graph-mcp Build and Deployment Targets"
	@echo "=========================================="
	@echo ""
	@echo "DEVELOPMENT TARGETS:"
	@echo "  install-deps          - Install Python dependencies"
	@echo "  run-local             - Run local MCP server (stdio)"
	@echo "  run-remote            - Run remote MCP server (HTTP on port 8548)"
	@echo "  test-remote           - Test the remote MCP server"
	@echo "  generate-config       - Generate client configuration for Cursor"
	@echo ""
	@echo "DOCKER COMPOSE TARGETS:"
	@echo "  docker-up             - Start server using docker-compose"
	@echo "  docker-down           - Stop and remove containers"
	@echo "  docker-logs           - View server logs"
	@echo "  docker-test           - Test dockerized server"
	@echo ""
	@echo "CONTEXT AND NAMESPACE MAPPING:"
	@echo "  local context → codekarma namespace (Local Kind cluster)"
	@echo "  ckqa context → codekarma namespace (CKQA environment)"
	@echo "  prod context → codekarma namespace (Production environment)"
	@echo "  gcp-fk-ckqa context → codekarma namespace (GCP FK CKQA environment)"
	@echo "  gcp-demo context → codekarma namespace (GCP Demo environment)"
	@echo "  flipkart context → codekarma namespace (Flipkart environment)"
	@echo ""
	@echo "DEPLOYMENT TARGETS:"
	@echo "  build-and-deploy-local          - Build and deploy to local Kind cluster"
	@echo "  build-and-deploy-ckqa - Build Docker image and deploy to CKQA environment"
	@echo "  build-and-deploy-prod  - Build Docker image and deploy to production environment"
	@echo "  build-and-deploy-gcp-fk-ckqa - Build Docker image and deploy to GCP FK CKQA environment"
	@echo "  build-and-deploy-gcp-demo   - Build Docker image and deploy to GCP Demo environment"
	@echo "  build-and-deploy-flipkart - Build Docker image and deploy to Flipkart environment"
	@echo "  deploy-ckqa           - Deploy existing image to CKQA environment"
	@echo "  deploy-prod           - Deploy existing image to production environment"
	@echo "  deploy-gcp-fk-ckqa    - Deploy existing image to GCP FK CKQA environment"
	@echo "  deploy-gcp-demo       - Deploy existing image to GCP Demo environment"
	@echo "  deploy-flipkart       - Deploy existing image to Flipkart environment"
	@echo ""
	@echo "BUILD-ONLY TARGETS:"
	@echo "  build-cleartrip       - Build Docker image for cleartrip environment (no deployment)"
	@echo "  build-flipkart        - Build Docker image for flipkart environment (no deployment)"
	@echo ""
	@echo "UTILITY TARGETS:"
	@echo "  check-credentials     - Verify Docker registry credentials"
	@echo "  setup-gradle-props    - Help set up gradle.properties file"
	@echo "  help-detailed         - Show comprehensive documentation"
	@echo ""
	@echo "For detailed documentation, run: make help-detailed"

# Development Targets
install-deps: ## Install Python dependencies
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

run-local: ## Run local MCP server (stdio)
	@echo "Starting local MCP server (stdio mode)..."
	@echo "Connect via Cursor MCP configuration with stdio transport"
	python mcp_server.py

run-remote: ## Run remote MCP server (HTTP)
	@echo "Starting remote MCP server on http://localhost:8548..."
	@echo "Endpoints:"
	@echo "  - Health: http://localhost:8548/health"
	@echo "  - MCP: http://localhost:8548/mcp"
	python remote_graph_mcp_server.py

test-remote: ## Test the remote MCP server
	@echo "Testing remote MCP server..."
	@if ! command -v python &> /dev/null; then \
		echo "Error: Python is not installed"; \
		exit 1; \
	fi
	@python test_remote_server.py http://localhost:8548

generate-config: ## Generate client configuration for Cursor
	@echo "Generating client configuration..."
	./generate-remote-config.sh

# Docker Compose Targets
docker-up: ## Start server using docker-compose
	@echo "Starting Graph MCP Server with docker-compose..."
	docker-compose up -d
	@echo "✅ Server started on http://localhost:8548"
	@echo "Run 'make docker-logs' to view logs"
	@echo "Run 'make docker-test' to test the server"

docker-down: ## Stop and remove containers
	@echo "Stopping Graph MCP Server..."
	docker-compose down
	@echo "✅ Server stopped"

docker-logs: ## View server logs
	docker-compose logs -f graph-mcp-server

docker-test: ## Test dockerized server
	@echo "Waiting for server to be ready..."
	@sleep 3
	@python test_remote_server.py http://localhost:8548

# Check Docker registry credentials
check-credentials: ## Verify that registry credentials are available
	@echo "Checking registry credentials..."
	@if [ -z "$(DOCKER_REGISTRY_USERNAME)" ] || [ -z "$(DOCKER_REGISTRY_TOKEN)" ]; then \
		echo "ERROR: Docker registry credentials not found!"; \
		echo ""; \
		echo "Please set one of the following:"; \
		echo "1. Environment variables:"; \
		echo "   export DOCKER_REGISTRY_USERNAME=your-github-username"; \
		echo "   export DOCKER_REGISTRY_TOKEN=your-github-personal-access-token"; \
		echo ""; \
		echo "2. Or set up gradle.properties file:"; \
		echo "   make setup-gradle-props"; \
		echo ""; \
		echo "Current values:"; \
		echo "  DOCKER_REGISTRY_USERNAME: $(DOCKER_REGISTRY_USERNAME)"; \
		echo "  DOCKER_REGISTRY_TOKEN: $(if $(DOCKER_REGISTRY_TOKEN),***hidden***,not set)"; \
		exit 1; \
	fi
	@echo "✓ Registry credentials found"
	@echo "  Username: $(DOCKER_REGISTRY_USERNAME)"
	@echo "  Token: ***hidden***"

# Help set up gradle.properties file
setup-gradle-props: ## Help set up gradle.properties file for registry credentials
	@echo "Setting up gradle.properties file for registry credentials..."
	@mkdir -p $(HOME)/.gradle
	@if [ ! -f $(GRADLE_PROPS_FILE) ]; then \
		echo "Creating $(GRADLE_PROPS_FILE)..."; \
		touch $(GRADLE_PROPS_FILE); \
	fi
	@echo ""
	@echo "Please edit $(GRADLE_PROPS_FILE) and set:"
	@echo "  gpr.user=your-github-username"
	@echo "  gpr.token=your-github-personal-access-token"

# Create Docker registry secret for specific environment
create-registry-secret: ## Create/update Docker registry secret for specific environment
	@echo "Creating/updating Docker registry secret for $(ENV) environment..."
	@kubectl create secret docker-registry ckn-ghcr-secret \
		--docker-server=$(DOCKER_REGISTRY) \
		--docker-username="$(DOCKER_REGISTRY_USERNAME)" \
		--docker-password="$(DOCKER_REGISTRY_TOKEN)" \
		--docker-email="$(DOCKER_REGISTRY_USERNAME)@codekarma.tech" \
		--namespace=codekarma \
		--save-config --dry-run=client -o yaml | kubectl apply -f -
	@echo "✓ Docker registry secret created/updated successfully"

# Context verification functions
verify-local-context: ## Verify kubectl context for local deployment
	@echo "Checking kubectl context for local deployment..."
	@CURRENT_CONTEXT=$$(kubectl config current-context); \
	if [[ "$$CURRENT_CONTEXT" != *"kind-"* ]]; then \
		echo "ERROR: Current kubectl context is '$$CURRENT_CONTEXT', not a Kind context."; \
		echo "Expected: A Kind cluster context (should contain 'kind-')"; \
		echo "Available contexts:"; \
		kubectl config get-contexts; \
		echo "To switch context, run:"; \
		echo "  kubectl config use-context <kind-context-name>"; \
		exit 1; \
	fi; \
	echo "✓ Current context is Kind: $$CURRENT_CONTEXT"

verify-ckqa-context: ## Verify kubectl context for CKQA deployment
	@echo "Checking kubectl context for CKQA deployment..."
	@CURRENT_CONTEXT=$$(kubectl config current-context); \
	if [[ "$$CURRENT_CONTEXT" != *"ck-qa"* ]]; then \
		echo "ERROR: Current kubectl context is '$$CURRENT_CONTEXT', not a CKQA context."; \
		echo "Expected: AWS CKQA cluster context (should contain 'ck-qa')"; \
		echo "Available contexts:"; \
		kubectl config get-contexts; \
		echo "To switch context, run:"; \
		echo "  kubectl config use-context <ckqa-context-name>"; \
		exit 1; \
	fi; \
	echo "✓ Current context is CKQA: $$CURRENT_CONTEXT"

verify-prod-context: ## Verify kubectl context for production deployment
	@echo "Checking kubectl context for production deployment..."
	@CURRENT_CONTEXT=$$(kubectl config current-context); \
	if [[ "$$CURRENT_CONTEXT" != *"ck-aws-prod"* ]]; then \
		echo "ERROR: Current kubectl context is '$$CURRENT_CONTEXT', not a production context."; \
		echo "Expected: AWS production cluster context (should contain 'ck-aws-prod')"; \
		echo "Available contexts:"; \
		kubectl config get-contexts; \
		echo "To switch context, run:"; \
		echo "  kubectl config use-context <prod-context-name>"; \
		exit 1; \
	fi; \
	echo "✓ Current context is Production: $$CURRENT_CONTEXT"

verify-gcp-fk-ckqa-context: ## Verify kubectl context for GCP FK CKQA deployment
	@echo "Checking kubectl context for GCP FK CKQA deployment..."
	@CURRENT_CONTEXT=$$(kubectl config current-context); \
	if [[ "$$CURRENT_CONTEXT" != *"gke_codekarma-auth_us-east1_ck-fk-pg"* ]]; then \
		echo "ERROR: Current kubectl context is '$$CURRENT_CONTEXT', not a GCP FK CKQA context."; \
		echo "Expected: GCP FK CKQA cluster context (should contain 'gke_codekarma-auth_us-east1_ck-fk-pg')"; \
		echo "Available contexts:"; \
		kubectl config get-contexts; \
		echo "To switch context, run:"; \
		echo "  kubectl config use-context <gcp-fk-ckqa-context-name>"; \
		exit 1; \
	fi; \
	echo "✓ Current context is GCP FK CKQA: $$CURRENT_CONTEXT"

verify-gcp-demo-context: ## Verify kubectl context for GCP Demo deployment
	@echo "Checking kubectl context for GCP Demo deployment..."
	@CURRENT_CONTEXT=$$(kubectl config current-context); \
	if [[ "$$CURRENT_CONTEXT" != "gke_resounding-node-471205-f9_us-east1_demo-cluster" ]]; then \
		echo "ERROR: Current kubectl context is '$$CURRENT_CONTEXT', not a GCP Demo context."; \
		echo "Expected: GCP Demo cluster context (should contain 'gke_codekarma-demo')"; \
		echo "Available contexts:"; \
		kubectl config get-contexts; \
		echo "To switch context, run:"; \
		echo "  kubectl config use-context <gcp-demo-context-name>"; \
		exit 1; \
	fi; \
	echo "✓ Current context is GCP Demo: $$CURRENT_CONTEXT"

verify-flipkart-context: ## Verify kubectl context for Flipkart deployment
	@echo "Checking kubectl context for Flipkart deployment..."
	@CURRENT_CONTEXT=$$(kubectl config current-context); \
	if [[ "$$CURRENT_CONTEXT" != "gke_fk-code-karma_asia-south1_gke-code-karma-prod-1" ]]; then \
		echo "ERROR: Current kubectl context is '$$CURRENT_CONTEXT', not a Flipkart context."; \
		echo "Expected: Flipkart cluster context (gke_fk-code-karma_asia-south1_gke-code-karma-prod-1)"; \
		echo "Available contexts:"; \
		kubectl config get-contexts; \
		echo "To switch context, run:"; \
		echo "  kubectl config use-context gke_fk-code-karma_asia-south1_gke-code-karma-prod-1"; \
		exit 1; \
	fi; \
	echo "✓ Current context is Flipkart: $$CURRENT_CONTEXT"

# Build and deploy to CKQA environment
build-and-deploy-ckqa: check-credentials verify-ckqa-context ## Build Docker image and deploy to CKQA environment
	@echo "Building Docker image and deploying to CKQA environment..."
	@$(MAKE) build-docker-image ENV=ckqa
	@$(MAKE) deploy-ckqa
	@echo "✓ CKQA build and deployment completed successfully"

# Build and deploy to production environment
build-and-deploy-prod: check-credentials verify-prod-context ## Build Docker image and deploy to production environment
	@echo "Building Docker image and deploying to production environment..."
	@$(MAKE) build-docker-image ENV=prod
	@$(MAKE) deploy-prod
	@echo "✓ Production build and deployment completed successfully"

# Build and deploy to GCP FK CKQA environment
build-and-deploy-gcp-fk-ckqa: check-credentials verify-gcp-fk-ckqa-context ## Build Docker image and deploy to GCP FK CKQA environment
	@echo "Building Docker image and deploying to GCP FK CKQA environment..."
	@$(MAKE) build-docker-image ENV=gcp-fk-ckqa
	@$(MAKE) deploy-gcp-fk-ckqa
	@echo "✓ GCP FK CKQA build and deployment completed successfully"

# Build and deploy to GCP Demo environment
build-and-deploy-gcp-demo: check-credentials verify-gcp-demo-context ## Build Docker image and deploy to GCP Demo environment
	@echo "Building Docker image and deploying to GCP Demo environment..."
	@$(MAKE) build-docker-image ENV=gcp-demo
	@$(MAKE) deploy-gcp-demo
	@echo "✓ GCP Demo build and deployment completed successfully"

# Build and deploy to Flipkart environment
build-and-deploy-flipkart: check-credentials verify-flipkart-context ## Build Docker image and deploy to Flipkart environment
	@echo "Building Docker image and deploying to Flipkart environment..."
	@$(MAKE) build-docker-image ENV=flipkart
	@$(MAKE) deploy-flipkart
	@echo "✓ Flipkart build and deployment completed successfully"

# Build and push Docker image for specific environment
build-docker-image: ## Build and push Docker image for specific environment
	@echo "Building Docker image for $(ENV) environment..."
	@echo "Using registry username: $(DOCKER_REGISTRY_USERNAME)"
	@echo "Logging into $(DOCKER_REGISTRY)..."
	@echo "$(DOCKER_REGISTRY_TOKEN)" | docker login $(DOCKER_REGISTRY) -u "$(DOCKER_REGISTRY_USERNAME)" --password-stdin
	@echo "Building multi-platform Docker image..."
	@docker buildx build --platform linux/amd64,linux/arm64 \
		-t $(DOCKER_REGISTRY)/$(DOCKER_REGISTRY_USERNAME)/$(ENV)/$(IMAGE_NAME)/$(IMAGE_NAME):latest \
		--push .
	@echo "✓ Docker image built and pushed for $(ENV) environment: $(DOCKER_REGISTRY)/$(DOCKER_REGISTRY_USERNAME)/$(ENV)/$(IMAGE_NAME)/$(IMAGE_NAME):latest"

# Build Docker image for cleartrip environment (build only, no deployment)
build-cleartrip: check-credentials ## Build Docker image for cleartrip environment (build only, no deployment)
	@echo "Building Docker image for cleartrip environment..."
	@$(MAKE) build-docker-image ENV=cleartrip

# Build Docker image for flipkart environment (build only, no deployment)
build-flipkart: check-credentials ## Build Docker image for flipkart environment (build only, no deployment)
	@echo "Building Docker image for flipkart environment..."
	@$(MAKE) build-docker-image ENV=flipkart

# Local Docker build for Kind cluster
dockerise-local: ## Build Docker image and load into local Kind cluster
	@echo "Building Docker image for local deployment..."
	@docker build -t $(IMAGE_NAME):latest .
	@echo "Loading image into Kind cluster..."
	@kind load docker-image $(IMAGE_NAME):latest --name=kind
	@echo "✓ Local docker image built and loaded successfully"

# Deployment targets (using unified common function)
deploy-ckqa: check-credentials verify-ckqa-context ## Deploy existing image to CKQA environment
	@$(MAKE) deploy-common ENV=ckqa

deploy-prod: check-credentials verify-prod-context ## Deploy existing image to production environment
	@$(MAKE) deploy-common ENV=prod

deploy-gcp-fk-ckqa: check-credentials verify-gcp-fk-ckqa-context ## Deploy existing image to GCP FK CKQA environment
	@$(MAKE) deploy-common ENV=gcp-fk-ckqa

deploy-gcp-demo: check-credentials verify-gcp-demo-context ## Deploy existing image to GCP Demo environment
	@$(MAKE) deploy-common ENV=gcp-demo

deploy-flipkart: check-credentials verify-flipkart-context ## Deploy existing image to Flipkart environment
	@echo "Deploying to Flipkart environment..."
	@$(MAKE) create-registry-secret ENV=flipkart
	@echo "Checking if existing release exists..."
	@if helm list -n codekarma | grep -q ck-graph-mcp; then \
		echo "Uninstalling existing ck-graph-mcp release..."; \
		helm uninstall ck-graph-mcp -n codekarma; \
		echo "Waiting for cleanup..."; \
		sleep 5; \
	else \
		echo "No existing release found, proceeding with fresh installation..."; \
	fi
	@echo "Installing fresh ck-graph-mcp release..."
	@helm install ck-graph-mcp-server ./charts/ck-graph-mcp-server-charts \
		--namespace codekarma \
		--create-namespace \
		--set image.repository="$(DOCKER_REGISTRY)/$(DOCKER_REGISTRY_USERNAME)/flipkart/$(IMAGE_NAME)/$(IMAGE_NAME)" \
		--set image.tag="latest" \
		--set image.pullPolicy="Always" \
		-f ./charts/ck-graph-mcp-server-charts/values-gcp-flipkart.yaml
	@echo "Waiting for ck-graph-mcp deployment to be ready..."
	@kubectl wait --for=condition=ready pod -l app=ck-graph-mcp -n codekarma --timeout=300s
	@echo "ck-graph-mcp deployed successfully"
	@sleep 3
	@echo "Restarting ck-ingress-nginx deployment..."
	@kubectl rollout restart deployment/ck-ingress-nginx -n codekarma
	@echo "Waiting for ingress controller to be ready..."
	@kubectl rollout status deployment/ck-ingress-nginx -n codekarma --timeout=120s
	@echo "✓ Flipkart deployment completed successfully"

# Local deployment to Kind cluster
build-and-deploy-local: verify-local-context dockerise-local ## Build and deploy to local Kind cluster
	@echo "Uninstalling ck-graph-mcp from local Kind cluster..."
	@helm uninstall ck-graph-mcp -n codekarma || true
	@sleep 4
	@echo "Installing ck-graph-mcp to local Kind cluster..."
	@helm install ck-graph-mcp ./charts/ck-graph-mcp-server-charts \
		--namespace codekarma \
		--create-namespace \
		--set image.repository="$(IMAGE_NAME)" \
		--set image.tag="latest" \
		--set image.pullPolicy="Never" \
		-f ./charts/ck-graph-mcp-server-charts/values.yaml
	@sleep 2
	@echo "✓ Local deployment completed successfully"

# Common deployment function (unified Helm command)
deploy-common: ## Common deployment function for all environments
	@echo "Deploying to $(ENV) environment..."
	@$(MAKE) create-registry-secret ENV=$(ENV)
	@echo "Checking if existing release exists..."
	@if helm list -n codekarma | grep -q ck-graph-mcp; then \
		echo "Uninstalling existing ck-graph-mcp release..."; \
		helm uninstall ck-graph-mcp -n codekarma; \
		echo "Waiting for cleanup..."; \
		sleep 5; \
	else \
		echo "No existing release found, proceeding with fresh installation..."; \
	fi
	@echo "Installing fresh ck-graph-mcp release..."
	@helm install ck-graph-mcp-server ./charts/ck-graph-mcp-server-charts \
		--namespace codekarma \
		--create-namespace \
		--set image.repository="$(DOCKER_REGISTRY)/$(DOCKER_REGISTRY_USERNAME)/$(ENV)/$(IMAGE_NAME)/$(IMAGE_NAME)" \
		--set image.tag="latest" \
		--set image.pullPolicy="Always" \
		-f ./charts/ck-graph-mcp-server-charts/values-$(ENV).yaml
	@echo "Waiting for ck-graph-mcp deployment to be ready..."
	@kubectl wait --for=condition=ready pod -l app=ck-graph-mcp -n codekarma --timeout=300s
	@echo "ck-graph-mcp deployed successfully"
	@sleep 3
	@echo "Restarting ck-ingress-nginx deployment..."
	@kubectl rollout restart deployment/ck-ingress-nginx -n codekarma
	@echo "Waiting for ingress controller to be ready..."
	@kubectl rollout status deployment/ck-ingress-nginx -n codekarma --timeout=120s
	@echo "✓ $(ENV) deployment completed successfully"

# Comprehensive help documentation
help-detailed:
	@echo "ck-graph-mcp Build and Deployment Makefile"
	@echo "==========================================="
	@echo ""
	@echo "OVERVIEW:"
	@echo "This Makefile provides targets for building Docker images and deploying ck-graph-mcp"
	@echo "to different environments (local Kind, CKQA, production, GCP FK CKQA, GCP Demo, Flipkart) using Helm."
	@echo ""
	@echo "DEPLOYMENT APPROACH:"
	@echo "HELM-BASED: Uses Helm charts with --set for image override"
	@echo ""
	@echo "ENVIRONMENT-SPECIFIC IMAGE PATHS:"
	@echo "  Local:    ck-graph-mcp:latest (loaded into Kind cluster)"
	@echo "  CKQA:     ghcr.io/sabareesh-ckt/ckqa/ck-graph-mcp/ck-graph-mcp:latest"
	@echo "  Production: ghcr.io/sabareesh-ckt/prod/ck-graph-mcp/ck-graph-mcp:latest"
	@echo "  GCP FK CKQA: ghcr.io/sabareesh-ckt/gcp-fk-ckqa/ck-graph-mcp/ck-graph-mcp:latest"
	@echo "  GCP Demo:   ghcr.io/sabareesh-ckt/gcp-demo/ck-graph-mcp/ck-graph-mcp:latest"
	@echo "  Flipkart: ghcr.io/sabareesh-ckt/flipkart/ck-graph-mcp/ck-graph-mcp:latest"
	@echo "  Cleartrip:  ghcr.io/sabareesh-ckt/cleartrip/ck-graph-mcp/ck-graph-mcp:latest"
	@echo ""
	@echo "CREDENTIALS:"
	@echo "Docker registry credentials are automatically loaded from:"
	@echo "  1. Environment variables: DOCKER_REGISTRY_USERNAME, DOCKER_REGISTRY_TOKEN"
	@echo "  2. Gradle properties file: ~/.gradle/gradle.properties (gpr.user, gpr.token)"
	@echo ""
	@echo "DEPLOYMENT TARGETS:"
	@echo "  build-and-deploy-local          - Build and deploy to local Kind cluster"
	@echo "  build-and-deploy-ckqa - Complete pipeline: build image + deploy to CKQA"
	@echo "  build-and-deploy-prod  - Complete pipeline: build image + deploy to production"
	@echo "  build-and-deploy-gcp-fk-ckqa - Complete pipeline: build image + deploy to GCP FK CKQA"
	@echo "  build-and-deploy-gcp-demo   - Complete pipeline: build image + deploy to GCP Demo"
	@echo "  build-and-deploy-flipkart - Complete pipeline: build image + deploy to Flipkart"
	@echo "  deploy-ckqa           - Deploy existing image to CKQA environment"
	@echo "  deploy-prod           - Deploy existing image to production environment"
	@echo "  deploy-gcp-fk-ckqa    - Deploy existing image to GCP FK CKQA environment"
	@echo "  deploy-gcp-demo       - Deploy existing image to GCP Demo environment"
	@echo "  deploy-flipkart       - Deploy existing image to Flipkart environment"
	@echo ""
	@echo "BUILD-ONLY TARGETS:"
	@echo "  build-cleartrip       - Build Docker image for cleartrip environment (no deployment)"
	@echo "  build-flipkart        - Build Docker image for flipkart environment (no deployment)"
	@echo ""
	@echo "UTILITY TARGETS:"
	@echo "  check-credentials     - Verify Docker registry credentials are available"
	@echo "  setup-gradle-props    - Help set up gradle.properties file"
	@echo ""
	@echo "CONTEXT VERIFICATION:"
	@echo "The following kubectl contexts are expected:"
	@echo "  Local:     Context containing 'kind-' (Kind cluster)"
	@echo "  CKQA:      Context containing 'ck-qa'"
	@echo "  Production: Context containing 'ck-aws-prod'"
	@echo "  GCP FK CKQA: Context containing 'gke_codekarma-auth_us-east1_ck-fk-pg'"
	@echo "  GCP Demo:   Context containing 'gke_codekarma-demo'"
	@echo "  Flipkart: Context 'gke_fk-code-karma_asia-south1_gke-code-karma-prod-1'"
	@echo ""
	@echo "EXAMPLES:"
	@echo "  # Build and deploy to local Kind cluster"
	@echo "  make build-and-deploy-local"
	@echo ""
	@echo "  # Build and deploy to CKQA environment"
	@echo "  make build-and-deploy-ckqa"
	@echo ""
	@echo "  # Build and deploy to production environment"
	@echo "  make build-and-deploy-prod"
	@echo ""
	@echo "  # Build and deploy to GCP FK CKQA environment"
	@echo "  make build-and-deploy-gcp-fk-ckqa"
	@echo ""
	@echo "  # Build and deploy to GCP Demo environment"
	@echo "  make build-and-deploy-gcp-demo"
	@echo ""
	@echo "  # Build and deploy to Flipkart environment"
	@echo "  make build-and-deploy-flipkart"
	@echo ""
	@echo "  # Deploy existing image to CKQA"
	@echo "  make deploy-ckqa"
	@echo ""
	@echo "  # Deploy existing image to GCP FK CKQA"
	@echo "  make deploy-gcp-fk-ckqa"
	@echo ""
	@echo "  # Deploy existing image to GCP Demo"
	@echo "  make deploy-gcp-demo"
	@echo ""
	@echo "  # Deploy existing image to Flipkart"
	@echo "  make deploy-flipkart"
	@echo ""
	@echo "  # Build image for cleartrip environment (no deployment)"
	@echo "  make build-cleartrip"
	@echo ""
	@echo "  # Build image for flipkart environment (no deployment)"
	@echo "  make build-flipkart"
	@echo ""
	@echo "  # Check if credentials are properly configured"
	@echo "  make check-credentials"
	@echo ""
	@echo "  # Set up gradle.properties file"
	@echo "  make setup-gradle-props"
	@echo ""
	@echo "NOTES:"
	@echo "- Helm approach: Uses '--set' to override image repository and tag"
	@echo "- Single command deployment with atomic updates"
	@echo "- Docker images are built for both linux/amd64 and linux/arm64 platforms"
	@echo "- Registry secrets are automatically created/updated in the codekarma namespace"
	@echo "- Helm provides better templating, rollback, and environment management"
	@echo "- GCP FK CKQA, GCP Demo, and Flipkart deployments use the same Helm chart with environment-specific values"

