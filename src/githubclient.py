from decouple import config
import requests
from src.urls import *
from src.models import ScriptItem, ScriptItems

GITHUB_API_KEY = config("GITHUB_API_KEY")


class Bearerauth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = "Bearer " + self.token
        return r


class GitHubClient:
    def __init__(self):
        self.client = requests.session()

    def get_tree_sha(self, tree_name: str = "scripts"):
        req = self.client.get(url=f"{GITHUB_API_TREES}/main", auth=Bearerauth(GITHUB_API_KEY))
        if req.status_code == requests.status_codes.codes.ok:
            for current_item in req.json()["tree"]:
                if current_item["path"] == tree_name:
                    return current_item["sha"]
        else:
            return None

    def get_all_setup_scripts(self, tree_name):
        req = self.client.get(url=f"{GITHUB_API_TREES}/{tree_name}", auth=Bearerauth(GITHUB_API_KEY))
        if req.status_code == requests.status_codes.codes.ok:
            items = []
            for current_script in req.json()["tree"]:
                name = current_script["path"].replace("setup-", "").replace(".sh", "")
                items.append(ScriptItem(name=name, path=f"{GITHUB_FILE_PATH}/{current_script['path']}"))
            items.sort()
            return ScriptItems(scripts=items)
        else:
            return None


if __name__ == "__main__":
    client = GitHubClient()
    print(client.get_all_setup_scripts(client.get_tree_sha()))
