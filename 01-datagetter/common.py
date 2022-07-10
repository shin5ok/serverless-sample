from db import MySpanner
import os

INSTANCE_ID: str = os.environ.get("INSTANCE_ID", "")
DATABASE_ID: str = os.environ.get("DATABASE_ID", "")
EXTERNAL_API: str = os.environ.get("EXTERNAL_API", "")

def is_valid_header():
    ...

def get_spanner():
    s = MySpanner(INSTANCE_ID, DATABASE_ID)
    yield s

def get_external_api_url():
    return os.environ.get("EXTERNAL_API", "")
