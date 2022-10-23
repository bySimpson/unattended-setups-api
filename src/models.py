import typing

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId
from decouple import config
import secrets


class APIStatus(BaseModel):
    message: str = "unattended-setups api is up and running!"
    version: str
    uptime: str


class ScriptItem(BaseModel):
    name: str
    path: str

    def __lt__(self, other):
        return self.name < other.name


class ScriptItems(BaseModel):
    scripts: list[ScriptItem]
