DATAGETTER_URL=localhost:8080
TRANSFORMER_URL=localhost:8081
REQUEST_URL=localhost:8082

ID=$(curl -s $DATAGETTER_URL/api/gen | jq .id -r)
echo $ID

FILE=$(echo "{\"id\":\"$ID\"}" | curl -X POST -H "Content-Type: application/json" $TRANSFORMER_URL/api/transform -d @- | jq .file -r)
echo $FILE

echo "{\"file\": \"$FILE\"}" | curl -X POST -H "Content-Type: application/json" $REQUESTER_URL/api/request -d @-

# gcloud workflows run $WORKFLOW_ID
