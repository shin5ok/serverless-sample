from fastapi import FastAPI, Depends, Request, Response, APIRouter
from pydantic import BaseModel, Field, EmailStr
from google.cloud import spanner
import requests
import logging
import sys
import uuid

from common import get_spanner, get_external_api_url

routers = APIRouter()

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class Response(BaseModel):
    name: str
    id: uuid.UUID


@routers.post("/{name}/{score}")
def _pathinfo(name: str, score: int, s = Depends(get_spanner)):
    id: str = s.insert_with_dml(name, score)
    return Response(id=id,name=name)

@routers.get("/gen")
def _main():
    response = requests.get(EXTERNAL_API)
    data: dict = json.loads(response.content)[0]
    s.insert_with_dml(data['name'], data['score'])
    return Response(id=100, name="tako")
