from ast import Slice
from multiprocessing.dummy import Array
from flask import Flask, request
import json
import os

from db import MySpanner

app: str = Flask(__name__)
instance_id: str = os.environ.get("INSTANCE_ID")
database_id: str = os.environ.get("DATABASE_ID")

@app.route("/test")
def _test() -> any:
    return f"{os.environ.get('K_SERVICE', 'local')} ok\n", 200

@app.route("/api/<string:name>/<int:age>", methods=["POST"])
def _main(name: str, age: str) -> any:
    s = MySpanner(instance_id, database_id)
    id: str = s.insert_with_dml(name, age)
    return json.dumps({"name":name, "id": id}, indent=2), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
