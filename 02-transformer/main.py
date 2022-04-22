from ast import Slice
from multiprocessing.dummy import Array
from flask import Flask, request
import json
import os
import pathlib
from datetime import datetime

from db import MySpanner
from gcs import MyGCS

app: str= Flask(__name__)
instance_id: str = os.environ.get("INSTANCE_ID")
database_id: str = os.environ.get("DATABASE_ID")
bucket_name: str = os.environ.get("BUCKET_NAME")

@app.route("/test")
def _test() -> any:
    return f"{os.environ.get('K_SERVICE', 'local')} ok\n", 200

@app.route("/api/transform/<string:id>", methods=["POST"])
def _main(id: str) -> any:
    json_file: str = f"{id}-{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    s = MySpanner(instance_id, database_id)
    result_data: list[str] = []

    code = 500
    try:
        for v in s.query_data(id):
            result_data.append(v)

        with open(json_file, "w") as f:
            f.write(json.dumps({"id":id, "data": result_data}))
        cs = MyGCS(bucket_name)
        cs.upload_blob(json_file, json_file)
        pathlib.Path(json_file).unlink()
        code = 200

    except Exception as e:
        print(str(e))

    return json.dumps({"file":json_file}),code


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
