import argparse
import base64
import datetime
import decimal
import json
import logging
import time

from google.cloud import spanner
from google.cloud.spanner_v1 import param_types

OPERATION_TIMEOUT_SECONDS = 240

class Datagetter:
    def __init__(self, instance_id, database_id):
        self.instance_id = instance_id
        self.database_id = database_id
        spanner_client = spanner.Client()
        instance = spanner_client.instance(instance_id)
        self.database = instance.database(database_id)


    def query_data(self, ):
        """Queries sample data from the database using SQL."""
        spanner_client = spanner.Client()
        instance = spanner_client.instance(instance_id)
        database = instance.database(database_id)

        with database.snapshot() as snapshot:
            results = snapshot.execute_sql(
                "SELECT SingerId, AlbumId, AlbumTitle FROM Albums"
            )

            for row in results:
                print(u"SingerId: {}, AlbumId: {}, AlbumTitle: {}".format(*row))