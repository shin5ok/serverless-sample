from ast import Slice
from multiprocessing.dummy import Array
import json
from fastapi import FastAPI, Depends
import os
import requests
from typing import Any
import routers.api, routers.test
import uvicorn

from db import MySpanner
from common import is_valid_header, get_spanner, get_external_api_url

app: Any = FastAPI()
PORT: int = os.environ.get("PORT", 8080)
app.include_router(routers.api.routers, prefix="/api", dependencies=[Depends(get_spanner),Depends(get_external_api_url)])
app.include_router(routers.test.routers)

if __name__ == '__main__':
    options = {
        'port': PORT, 
        'host': '0.0.0.0',
        'workers': 2,
        'reload': True,
    }
    uvicorn.run("main:app", **options)

#@app.route("/test")
#def _test() -> Any:
#    return f"{os.environ.get('K_SERVICE', 'local')} ok\n", 200
#
#@app.route("/api/<string:name>/<int:score>", methods=["POST"])
#def _pathinfo(name: str, score: int) -> Any:
#    s = MySpanner(INSTANCE_ID, DATABASE_ID)
#    id: str = s.insert_with_dml(name, score)
#    return jsonify({"name":name, "id": id}), 200
#
#@app.route("/api/gen")
#def _main() -> Any:
#    response = requests.get(EXTERNAL_API)
#    data: dict = json.loads(response.content)[0]
#    s = MySpanner(INSTANCE_ID, DATABASE_ID)
#    id: str = s.insert_with_dml(data['name'], data['score'])
#    return jsonify({"name":data['name'], "id": id}), 200


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
