from fastapi import FastAPI, Depends, Request, Response, APIRouter, Header
from pydantic import BaseModel, Field, EmailStr
from google.cloud import spanner
import requests
import logging
import sys
import uuid

routers = APIRouter()

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class TestRequest(BaseModel):
    id: int
    message: str

class TestResponse(BaseModel):
    return_message: str

@routers.post("/")
def _post(request: TestRequest, user_agent = Header(default = None), host = Header(default = None)):
    return_message = f"{request.dict()['message']} (user_agent: {user_agent}, host: {host})"
    return TestResponse(return_message=return_message)

@routers.get("/")
def _get():
    return dict(message="pong")
