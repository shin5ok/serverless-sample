from flask import Flask, request
import json
import os

from db import MySpanner

app = Flask(__name__)
instance_id = os.environ.get("INSTANCE_ID")
database_id = os.environ.get("DATABASE_ID")

@app.route("/test")
def _test():
    return "ok\n", 200

@app.route("/api/<string:name>/<int:age>")
def _root(name, age):
    s = MySpanner(instance_id, database_id)
    s.insert_with_dml(name, age)
    return json.dumps({}, indent=2), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
