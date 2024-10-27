# Makefile for deploying the infrastructure

.PHONY: deploy-infra clean

deploy-infra:
	@echo "Building the SAM application..."
	@sam build || { echo "SAM build failed"; exit 1; }
	@echo "Deploying the SAM application using aws-vault..."
	@aws-vault exec laptop_t --no-session -- sam deploy --no-confirm-changeset || { echo "SAM deploy failed"; exit 1; }

clean:
	@echo "Cleaning up previous SAM build artifacts..."
	@sam delete || { echo "Cleanup failed"; exit 1; }
