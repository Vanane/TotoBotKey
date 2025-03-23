from sys import argv
import os
import subprocess
from configparser import ConfigParser
import requests


class Publish:
    cp_config:ConfigParser
    cp_toml:ConfigParser

    github_api:str
    api_key:str
    last_version:str

    version_match:str

    version:str


    def __init__(self):
        self.cp_config = ConfigParser()
        self.cp_config.read(".config")

        self.github_api = self.cp_config["github"]["github_api"]
        self.api_key = self.cp_config["github"]["api_key"]
        self.api_version = self.cp_config["github"]["api_version"]

        self.https = self.cp_config["github"]["https"].replace("{api_key}", self.api_key)
        
        self.version_match = self.cp_config["version"]["version_match"]

        self.cp_toml = ConfigParser()
        self.cp_toml.read("pyproject.toml")
        
        self.last_version = self.cp_toml["project"]["version"]


    def get_version(self):
        return input(f"Version number :\n(last was v{self.last_version})").replace(' ', '_')


    def publish(self):
        # Stash any changes
        stashed = False
        stash_message = "Stashing for publication"
        stashed = str(subprocess.check_output(["git", "stash", "-m", stash_message])).find("Stashing for publication")

        # Get version number
        self.version = self.get_version()

        vversion = f"v{self.version}"

        print(f"Publishing TotoBotKey v{self.version}")

        # Make a new branch
        os.system(f"git checkout -b v{self.version}")

        # Update version number
        with open("pyproject.toml", "w", encoding="utf-8") as toml:
            self.cp_toml['project']['version'] = f"'{self.version}'"
            self.cp_toml.write(toml)

        # Commit & push the TOML file
        os.system("git add ./*")
        os.system(f"git commit -m \"Update to version {self.version}\"")
        os.system(f"git push --set-upstream {self.https} {vversion}")

        # Make a tag from the top commit
        commit = subprocess.check_output(['git','rev-parse', 'HEAD'])
        self.create_release(commit, vversion)

        # Build & publish
        os.system('make build')
        os.system('python3 -m twine upload dist/*')

        # Unstash changes
        if stashed:
            os.system('git stash pop')


    def create_release(self, commit:str, name:str):
        r = self.post_github("/releases", {
            "tag_name":name,
            "target_commitish":commit.strip()
        })

        if not r.ok:
            raise requests.HTTPError(f"{r.status_code} : {r.text}")


    def post_github(self, endpoint, body):
        return requests.post(f"{self.github_api}{endpoint}", json=body,
        headers = {
            "Accept":"application/vnd.github+json",
            "Authorization":f"Bearer {self.api_key}",
            "X-Github-Api-Version":self.api_version
        },
        timeout = 30)

    def get_github(self, endpoint, params:dict):
        return requests.get(f"{self.github_api}{endpoint}{"?" + "&".join([f"{str(p)}={str(params[p])}" for p in params.keys()]) if params is not None else ""}",
        headers = {
            "Accept":"application/vnd.github+json",
            "Authorization":f"Bearer {self.api_key}",
            "X-Github-Api-Version":self.api_version
        },
        timeout = 30)

if __name__ == '__main__':
    Publish().publish()
