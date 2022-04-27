from flask import Flask, jsonify, request
import json
import os
import pathlib
from datetime import datetime

from typing import Any

from db import MySpanner
# from db import MySpanner
from gcs import MyGCS

app: Any = Flask(__name__)
INSTANCE_ID: str = os.environ.get("INSTANCE_ID")
DATABASE_ID: str = os.environ.get("DATABASE_ID")
BUCKET_NAME: str = os.environ.get("BUCKET_NAME")

@app.route("/test")
def _test() -> Any:
    return f"{os.environ.get('K_SERVICE', 'local')} ok\n", 200

@app.route("/api/transform", methods=["POST"])
def _main() -> Any:
    posted: dict = request.get_json()
    id: str = posted['id']
    json_file: str = f"{id}-{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    result_data: list[str] = []

    code = 500
    try:
        s = MySpanner(INSTANCE_ID, DATABASE_ID)
        for v in s.query_data(id):
            conv_v: dict = {"id": v[0], "name":v[1], "score":v[2] * 2}
            result_data.append(conv_v)

        with open(json_file, "w") as f:
            f.write(json.dumps({"data": result_data}))
        cs = MyGCS(BUCKET_NAME)
        cs.upload_blob(json_file, json_file)
        pathlib.Path(json_file).unlink()
        code = 200

    except Exception as e:
        print(str(e))

    return jsonify({"file":json_file}),code


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
