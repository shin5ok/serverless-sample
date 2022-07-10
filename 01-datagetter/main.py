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

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
