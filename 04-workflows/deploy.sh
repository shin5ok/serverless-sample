set -eu

envsubst < templates/workflows.yaml > /tmp/workflows.yaml
SERVICE_ACCOUNT=workflows
gcloud workflows deploy workflow \
--source=/tmp/workflows.yaml \
--location=us-central1 \
--service-account=${SERVICE_ACCOUNT}@$PROJECT.iam.gserviceaccount.com
rm -f /tmp/workflow.yaml
