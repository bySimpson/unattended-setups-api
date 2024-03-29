import datetime
import humanize
import requests


from fastapi import FastAPI, HTTPException, Response
from starlette.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every
from api_analytics.fastapi import Analytics
from decouple import config
from src.models import APIStatus, ScriptItems
from src.githubclient import GitHubClient



version = config("VERSION", default="DEV", cast=str)
analytics = config("ANALYTICS_KEY", default="", cast=str)
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

if analytics != "":
    app.add_middleware(Analytics, api_key=analytics)


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

@app.get("/cli/{branch}",
         summary="Get CLI tool for specified branch",
         tags=["Setup"])
async def get_install_script_for_branch(branch: str):
    if branch == "":
        branch = "main"
    script = f"""#!/usr/bin/env bash

set -e
wget "https://github.com/bySimpson/unattended-setups/releases/download/{branch}/unattended-setups-$(uname -m)-unknown-linux-gnu.tar.gz" -O - | tar -xz
chmod +x unattended-setups
./unattended-setups && ProcessID=$!
wait $ProcessID
shred -u -f ./unattended-setups"""
    return Response(content=script, media_type="text")

@app.on_event("startup")
@repeat_every(seconds=60 * 5)
def update_monitoring():
    m_url = config("MONITORING_URL", default="", cast=str)
    if m_url:
      requests.get(m_url)  
