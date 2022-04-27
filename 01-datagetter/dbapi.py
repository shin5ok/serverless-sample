import uuid

from google.cloud.spanner_dbapi import connect
from typing import Any

class MySpanner:

    def __init__(self, instance_id: str, database_id: str) -> None:
        self.instance_id = instance_id
        self.database_id = database_id
        connection = connect(self.instance_id, self.database_id)
        self.connection = connection

    def __del__(self) -> None:
        self.connection.close()

    def query_data(self, id: str) -> Any:
        connection = self.connection
        cursor = connection.cursor()
        cursor.execute("""SELECT id,name,score FROM test WHERE id=%s""", [id])
        results: list[Any] = cursor.fetchall()
        connection.close()
        return results
    
    def insert_with_dml(self, name: str, score: int) -> str:
        connection = self.connection
        connection.autocommit = True
        cursor = connection.cursor()
        id: str = str(uuid.uuid4())
        # !!! You must use secure query in production, like sql placeholder !!!
        sql: str = f"INSERT into test (id, name, score) VALUES ('{id}', '{name}', {score})"
        print(sql)
        cursor.execute(sql)
        connection.close()
        return id

if __name__ == '__main__':
    import sys
    instance_id, database_id = sys.argv[1:3]
    print(instance_id, database_id)
    s = MySpanner(instance_id, database_id)
    id = s.insert_with_dml("foo", 100)
    for v in s.query_data(id):
        print(v)