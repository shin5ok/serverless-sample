BUCKET_NAME=$PROJECT
gcloud run deploy --source=. --set-env-vars=BUCKET_NAME=$BUCKET_NAME,SLACK_API=$SLACK_API --region=us-central1 requester
