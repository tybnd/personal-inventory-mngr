make deploy-infra: 
	sam build && aws-vault exec laptop_t --no-session sam deploy --no-confirm-changeset