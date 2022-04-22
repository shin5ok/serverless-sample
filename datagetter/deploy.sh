gcloud run deploy --source=. --set-env-vars=INSTANCE_ID=$INSTANCE_ID,DATABASE_ID=$DATABASE_ID --region=us-central1 datagetter --allow-unauthenticated
