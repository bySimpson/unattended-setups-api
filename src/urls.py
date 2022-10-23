from decouple import config

GITHUB_USERNAME = config("GITHUB_USERNAME")
GITHUB_REPOSITORY = config("GITHUB_REPOSITORY")
GITHUB_API_BASE = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPOSITORY}"
GITHUB_API_TREES = f"{GITHUB_API_BASE}/git/trees"
GITHUB_FILE_PATH = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{GITHUB_REPOSITORY}/main/scripts"
