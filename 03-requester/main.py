from ast import Slice
from distutils import file_util
from multiprocessing.dummy import Array
from flask import Flask, jsonify, request
import json
import os
from slack_sdk.webhook import WebhookClient
import pathlib

from gcs import MyGCS

BUCKET_NAME: str = os.environ.get("BUCKET_NAME")
SLACK_API: str = os.environ.get("SLACK_API")

app: str = Flask(__name__)

@app.route("/test")
def _test() -> any:
    return f"{os.environ.get('K_SERVICE', 'local')} ok\n", 200

@app.route("/api/request", methods=["POST"])
def _main() -> any:
    posted: dict = request.get_json()
    file: str = posted['file']
    cs: MyGCS = MyGCS(BUCKET_NAME)
    cs.download_blob(file, file)
    with open(file) as f:
        data = json.loads(f.read())
        webhook = WebhookClient(SLACK_API)
        response = webhook.send(text=data['id'])
        pathlib.Path(file).unlink()
    return jsonify({}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
