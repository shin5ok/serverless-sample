from ast import Slice
from distutils import file_util
from multiprocessing.dummy import Array
from flask import Flask, jsonify, request
import json
import os
from slack_sdk.webhook import WebhookClient
import pathlib

from typing import Any

from gcs import MyGCS

BUCKET_NAME: str = os.environ.get("BUCKET_NAME")
SLACK_API: str = os.environ.get("SLACK_API")

app: Any = Flask(__name__)

@app.route("/test")
def _test() -> Any:
    return f"{os.environ.get('K_SERVICE', 'local')} ok\n", 200

@app.route("/api/request", methods=["POST"])
def _main() -> Any:
    posted: dict = request.get_json()
    file: str = posted['file']
    cs: MyGCS = MyGCS(BUCKET_NAME)
    cs.download_blob(file, file)
    with open(file) as f:
        data = json.loads(f.read())
        send_data: str = [x["id"] for x in data["data"]]

        webhook = WebhookClient(SLACK_API)
        response = webhook.send(text=",".join(send_data))

        pathlib.Path(file).unlink()
    return jsonify({}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
