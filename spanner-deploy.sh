gcloud beta spanner instances create --config=regional-us-central1 --processing-units=100 test-instance --description="$PROJECT"
gcloud beta spanner databases create --instance=test-instance testdb

cmd="spanner-cli -i test-instance -d testdb -p $PROJECT"

cat <<'EOD' | $cmd

CREATE TABLE test (id STRING(36) NOT NULL,name STRING(64), score INT64) PRIMARY KEY(id);

EOD
