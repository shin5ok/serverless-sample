from ast import Slice
from multiprocessing.dummy import Array
from flask import Flask, jsonify, request
import json
import os

from db import MySpanner

app: str = Flask(__name__)
instance_id: str = os.environ.get("INSTANCE_ID")
database_id: str = os.environ.get("DATABASE_ID")

@app.route("/test")
def _test() -> any:
    return f"{os.environ.get('K_SERVICE', 'local')} ok\n", 200

@app.route("/api/<string:name>/<int:score>", methods=["POST"])
def _main(name: str, score: str) -> any:
    s = MySpanner(instance_id, database_id)
    id: str = s.insert_with_dml(name, score)
    return jsonify({"name":name, "id": id}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
