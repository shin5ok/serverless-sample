BUCKET_NAME=$PROJECT
gcloud run deploy --source=. --set-env-vars=INSTANCE_ID=$INSTANCE_ID,DATABASE_ID=$DATABASE_ID,BUCKET_NAME=$BUCKET_NAME --region=us-central1 transformer
