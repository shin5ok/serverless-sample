import argparse
import base64
import datetime
import decimal
import json
import logging
import time
from uuid import uuid4

from typing import Any

from google.cloud import spanner
from google.cloud.spanner_v1 import param_types

OPERATION_TIMEOUT_SECONDS: int = 240


class MySpanner:

    def __init__(self, instance_id: str, database_id: str) -> None:
        spanner_client = spanner.Client()
        instance = spanner_client.instance(instance_id)
        self.database = instance.database(database_id)


    def query_data(self, id: str) -> Any:
        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql(
                "SELECT id,name,score from test where id = @id",
                params={"id": id},
                param_types={"id": spanner.param_types.STRING}
            )
        return results

    def insert_with_dml(self, name: str, score: int) -> Any:

        def insert_record(transaction) -> str:

            id: str = str(uuid4())
            row_ct = transaction.execute_update(
                "INSERT test (id, name, score) VALUES (@id, @name, @score)",
                params={"id":id, "name":name, "score":score},
                param_types={"name": spanner.param_types.STRING, "id": spanner.param_types.STRING, "score": spanner.param_types.INT64}
            )
            print("{} record(s) inserted.".format(row_ct))
            return id

        return self.database.run_in_transaction(insert_record)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("instance_id", type=str)
    parser.add_argument("database_id", type=str)
    args = parser.parse_args()
    print(args.instance_id, args.database_id)
    s = MySpanner(args.instance_id, args.database_id)
    import random
    s.insert_with_dml("foo", random.randrange(100))
    for v in s.query_data("foo"):
        print(v)
