import base64
import dataclasses
import datetime
import json

import isodate
import requests
import yaml

from torque_bulk_deployer.consts import TORQUE_API_BASE


class TorqueAPIClient(object):
    api_token: str
    refresh_token: str
    token_expiration: datetime.datetime
    account_name: str
    auth_headers: dict = {}

    def __init__(self, account_name: str, username: str, password: str, password_type: str, auth_token: str):
        if auth_token:
            self.api_token = auth_token
            self.account_name = account_name
        else:
            self.login(account_name, username, password if password_type == "plain" else base64.decodestring(password))

        self.auth_headers = {"Authorization": f"Bearer {self.api_token}"}

    def login(self, account_name, username, password):
        request_time = datetime.datetime.now()
        login_response = requests.post(f"{TORQUE_API_BASE}/accounts/login", json={"email": username, "password": password})
        login_response_json = json.loads(login_response.content)
        if account_name == "":
            account_name = list(login_response_json[0].keys())[0]

        login_response_data = login_response_json[account_name]

        self.api_token = login_response_data["access_token"]
        self.refresh_token = login_response_data["refresh_token"]
        self.token_expiration = request_time + datetime.timedelta(seconds=login_response_data["expires_in"])
        self.account_name = account_name

    def get_blueprints(self, space_name, published_only: bool = False):
        get_bps_response = requests.get(f"{TORQUE_API_BASE}/spaces/{space_name}/blueprints", headers=self.auth_headers)
        get_bps_response_json = json.loads(get_bps_response.content)
        short_blueprints_list = [BlueprintShortInfo(blueprint["name"], blueprint["description"], blueprint["url"], blueprint["labels"])
                                 for blueprint in get_bps_response_json
                                 if (blueprint["enabled"] and published_only) or (not published_only)]
        return yaml.dump(short_blueprints_list, sort_keys=False)

    def create_environment(self, space_name, environment_name, duration_in_minutes: int, blueprint_name, description, owner, repository_name, collaborators: list[str] = [], blueprint_inputs: dict[str, str] = {}) -> str:
        request_data = {"environment_name": environment_name,
                        "blueprint_name": blueprint_name,
                        "owner_email": owner,
                        "description": description,
                        "duration": isodate.duration_isoformat(isodate.Duration(minutes=duration_in_minutes)),
                        "collaborators": {"collaborators_emails": collaborators, "all_space_members": False},
                        "automation": True,
                        "inputs": blueprint_inputs,
                        "source": {"repository_name": repository_name}}
        create_env_response = requests.post(f"{TORQUE_API_BASE}/spaces/{space_name}/environments", headers=self.auth_headers,
                                            json=request_data)
        try:
            env_id = json.loads(create_env_response.content)["id"]
            return env_id
        except Exception as ex:
            raise Exception(f"create environment failed with message {create_env_response.content}") from ex


@dataclasses.dataclass
class BlueprintShortInfo:
    name: str
    description: str
    url: str
    labels: list[dict]
