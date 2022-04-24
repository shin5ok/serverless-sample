import uuid

from google.cloud.spanner_dbapi import connect

class MySpanner:

    def __init__(self, instance_id: str, database_id: str) -> None:
        self.instance_id = instance_id
        self.database_id = database_id

    def query_data(self, id: str) -> any:
        connection = connect(self.instance_id, self.database_id)
        cursor = connection.cursor()
        cursor.execute("""SELECT id,name,score FROM test WHERE id=%s""", [id])
        results: list[any] = cursor.fetchall()
        connection.close()
        return results
    
    def insert_with_dml(self, name: str, score: int) -> str:
        connection = connect(self.instance_id, self.database_id)
        connection.autocommit = True
        cursor = connection.cursor()
        id: str = uuid.uuid4()
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
    for v in s.query_data(str(id)):
        print(v)