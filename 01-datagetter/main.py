from ast import Slice
from multiprocessing.dummy import Array
from flask import Flask, jsonify, request
import json
import os
import requests

# from db import MySpanner
from db import MySpanner

app: any = Flask(__name__)
INSTANCE_ID: str = os.environ.get("INSTANCE_ID")
DATABASE_ID: str = os.environ.get("DATABASE_ID")
EXTERNAL_API: str = os.environ.get("EXTERNAL_API")

@app.route("/test")
def _test() -> any:
    return f"{os.environ.get('K_SERVICE', 'local')} ok\n", 200

@app.route("/api/<string:name>/<int:score>", methods=["POST"])
def _pathinfo(name: str, score: str) -> any:
    s = MySpanner(INSTANCE_ID, DATABASE_ID)
    id: str = s.insert_with_dml(name, score)
    return jsonify({"name":name, "id": id}), 200

@app.route("/api/gen")
def _main() -> any:
    response = requests.get(EXTERNAL_API)
    data = json.loads(response.content)[0]
    s = MySpanner(INSTANCE_ID, DATABASE_ID)
    id: str = s.insert_with_dml(data['name'], data['score'])
    return jsonify({"name":data['name'], "id": id}), 200


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
