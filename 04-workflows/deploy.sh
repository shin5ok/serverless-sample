set -eu

envsubst < templates/workflows.yaml > /tmp/workflow.yaml
SERVICE_ACCOUNT=workflows
gcloud workflows deploy workflow \
--source=/tmp/workflows.yaml \
--service-account=${SERVICE_ACCOUNT}@$PROJECT.iam.gserviceaccount.com
rm -f /tmp/workflow.yaml