gcloud run deploy --source=. --set-env-vars=INSTANCE_ID=$INSTANCE_ID,DATABASE_ID=$DATABASE_ID,EXTERNAL_API=$EXTERNAL_API --region=us-central1 datagetter
