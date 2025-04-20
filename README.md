# unattended-setups-api
This repository contains an api that automatically fetches all unattended setup scripts and serves them in a json array.

# deployment
This project can both be deployed using docker or standalone.
## run it locally
````shell
python3 -m pip install -r requirements.txt
python3 main.py
````
## run with docker
````docker
doker run -p 8080:8080 \
    -e GITHUB_USERNAME=bySimpson \ 
    -e GITHUB_REPOSITORY=unattended-setups \
    -e GITHUB_API_KEY=YOUR_API_KEY ghcr.io/bysimpson/unattended-setups-api:latest
````