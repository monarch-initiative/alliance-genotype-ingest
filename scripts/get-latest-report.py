import requests
import json


# https://github.com/monarch-initiative/alliance_genotype/releases/latest/download/report.md
def get_latest_release_file(user, repo, filename):
    url = f"https://api.github.com/repos/monarch-initiative/alliance_genotype/releases/latest"
    response = requests.get(url)
    data = json.loads(response.text)

    for asset in data["assets"]:
        if asset["name"] == "report.md":
            file_url = asset["browser_download_url"]
            return file_url

    return None


# Usage
user = "username"
repo = "repository"
filename = "file.ext"
print(get_latest_release_file(user, repo, filename))
