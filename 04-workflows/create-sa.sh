SERVICE_ACCOUNT=workflows
gcloud iam service-accounts create $SERVICE_ACCOUNT
gcloud projects add-iam-policy-binding $PROJECT \
    --member "serviceAccount:${SERVICE_ACCOUNT}@$PROJECT.iam.gserviceaccount.com" \
    --role "roles/run.invoker"
echo $SERVICE_ACCOUNT