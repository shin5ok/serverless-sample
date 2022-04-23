SERVICE_ACCOUNT=workflows
gcloud workflows deploy workflow \
--source=workflows.yaml \
--service-account=${SERVICE_ACCOUNT}@$PROJECT.iam.gserviceaccount.com