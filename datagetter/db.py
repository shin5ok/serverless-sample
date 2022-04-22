import argparse
import base64
import datetime
import decimal
import json
import logging
import time
from uuid import uuid4

from google.cloud import spanner
from google.cloud.spanner_v1 import param_types

OPERATION_TIMEOUT_SECONDS = 240

class MySpanner:

    def __init__(self, instance_id, database_id):
        spanner_client = spanner.Client()
        instance = spanner_client.instance(instance_id)
        self.database = instance.database(database_id)


    def query_data(self, name: str) -> any:
        with self.database.snapshot() as snapshot:
            results = snapshot.execute_sql(
                "SELECT id,name,age from test where name = @name",
                params={"name": name},
                param_types={"name": spanner.param_types.STRING}
            )
        return results

    def insert_with_dml(self, name: str, age: int) -> None: 

        def insert_record(transaction):
            id = str(uuid4())
            row_ct = transaction.execute_update(
                "INSERT test (id, name, age) VALUES (@id, @name, @age)",
                params={"id":id, "name":name, "age":age},
                param_types={"name": spanner.param_types.STRING, "id": spanner.param_types.STRING, "age": spanner.param_types.INT64}
            )
            print("{} record(s) inserted.".format(row_ct))

        self.database.run_in_transaction(insert_record)

if __name__ == '__main__':
    import sys
    instance_id, database_id = sys.argv[1:3]
    print(instance_id, database_id)
    s = MySpanner(instance_id, database_id)
    s.insert_with_dml("foo", 100)
    for v in s.query_data("foo"):
        print(v)
