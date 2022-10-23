import datetime
import humanize

from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from decouple import config
from src.models import APIStatus, ScriptItems
from src.githubclient import GitHubClient

version = config("VERSION", default="DEV", cast=str)
start_time = datetime.datetime.now()
github_client = GitHubClient()

if version == "%VER%":
    version = "DEV"

app = FastAPI(
    title="unattended-setups API",
    version=version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/",
         summary="Check service status",
         response_model=APIStatus,
         tags=["Status"])
async def root() -> APIStatus:
    time_delta = datetime.datetime.now() - start_time
    output_time = humanize.naturaldelta(time_delta)
    return APIStatus(version=version, uptime=output_time)


@app.get("/setup/all",
         summary="Get all available setups",
         response_model=ScriptItems,
         tags=["Setup"])
async def get_all_setups():
    sha = github_client.get_tree_sha()
    if sha:
        return github_client.get_all_setup_scripts(sha)
    return HTTPException(404, "No scripts found!")