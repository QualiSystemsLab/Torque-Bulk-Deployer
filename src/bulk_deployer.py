import datetime
import json
import os
import sys
from threading import Thread

import consts
from torque_api_client import TorqueAPIClient


class TorqueDeployerApp:
    auth_token:    str = ""
    auth_username: str = ""
    auth_password: str = ""
    api_client:    TorqueAPIClient = None

    def __init__(self, command_line_args=None):
        self.cli_args_dict = command_line_args

    def main(self):
        # print(args_dictionary)
        if "--help" in self.cli_args_dict:
            self.print_help_instructions()
            exit(0)

        if not self.api_client:
            self.init_api_client()

        if "get_blueprints" in self.cli_args_dict:
            self.display_blueprints()
            exit(0)

        if "start_environments" in self.cli_args_dict:
            self.start_environments()
            exit(0)

        if "start_environment" in self.cli_args_dict:
            self.start_environment()
            exit(0)

    def print_help_instructions(self):
        if "get_blueprints" in self.cli_args_dict:
            print(consts.GET_BLUEPRINTS_HELP)
        elif "start_environments" in self.cli_args_dict:
            print(consts.START_ENVIRONMENTS_HELP)
        elif "start_environment" in self.cli_args_dict:
            print(consts.START_ENVIRONMENT_HELP)
        else:
            print(consts.HELP_TEXT)

    def init_api_client(self):
        if os.path.isfile(self.cli_args_dict.get("--config_file", "")):
            with open(self.cli_args_dict["--config_file"], "r") as jsonconfigfile:
                jsonconfig = json.load(jsonconfigfile)

            auth_token = jsonconfig.get("auth_token", "")
            username = jsonconfig.get("username", "")
            password = jsonconfig.get("password", "")
            account_name = jsonconfig.get("account", "")
        else:
            auth_token = self.cli_args_dict.get("--auth_token", "")
            username = self.cli_args_dict.get("--username", "")
            password = self.cli_args_dict.get("--password", "")
            account_name = self.cli_args_dict.get("--account", "")

        self.api_client = TorqueAPIClient(account_name, username, password, "plain", auth_token)

    def display_blueprints(self):
        if "--published_only" in self.cli_args_dict:
            published_only = (self.cli_args_dict["--published_only"].lower() == "true")
        else:
            published_only = False

        space_name = self.cli_args_dict["--space_name"]

        blueprints = self.api_client.get_blueprints(space_name, published_only)
        print(blueprints)

    def start_environment(self):
        space_name = self.cli_args_dict["--space_name"]
        source_repo_name = self.cli_args_dict.get("--source_repo", "qtorque")
        blueprint_name = self.cli_args_dict.get("--blueprint", "")
        if source_repo_name == "qtorque":
            blueprint_name = "autogen_" + blueprint_name

        env_name = self.cli_args_dict.get("--environment_name", blueprint_name + str(datetime.datetime.utcnow()))

        env_description = self.cli_args_dict.get("--description", "")
        env_owner = self.cli_args_dict["--owner"]
        env_inputs_str = self.cli_args_dict.get("--inputs", "")
        env_inputs = {env_input.split(":")[0]: env_input.split(":")[1] for env_input in env_inputs_str.split(",")}
        duration_minutes = int(self.cli_args_dict.get("--duration", 10))
        collaborators = self.cli_args_dict.get("--collaborators", "")
        if collaborators:
            collaborators = collaborators.split(";")

        env_id = self.api_client.create_environment(space_name, env_name, duration_minutes, blueprint_name, env_description, env_owner,
                                                    source_repo_name, collaborators, env_inputs)
        print(f"Created environment {env_name} with id {env_id}")

    def start_environments(self):
        space_name = self.cli_args_dict["--space_name"]
        source_repo_name = self.cli_args_dict.get("--source_repo", "qtorque")
        blueprint_name = self.cli_args_dict.get("--blueprint", "")
        if source_repo_name == "qtorque":
            blueprint_name = "autogen_" + blueprint_name

        env_description = self.cli_args_dict.get("--description", "")
        env_inputs_str = self.cli_args_dict.get("--inputs", "")
        env_inputs = {env_input.split(":")[0]: env_input.split(":")[1] for env_input in env_inputs_str.split(",")}
        duration_minutes = int(self.cli_args_dict.get("--duration", 10))

        env_owners = self.cli_args_dict["--owners"].split(";")

        env_creation_threads = []
        results_dictionary = {}
        for owner in env_owners:
            env_name = f"My Env - {owner}"
            create_env_args = (space_name, env_name, duration_minutes, blueprint_name, env_description, owner, source_repo_name, [], env_inputs, results_dictionary)
            env_creation_threads.append(Thread(target=self.create_environment_executor, args=create_env_args))

        joined_threads = 0
        while joined_threads < len(env_creation_threads):
            current_pool = []
            for _ in range(5):
                if env_creation_threads:
                    current_thread = env_creation_threads.pop()
                    current_thread.start()
                    current_pool.append(current_thread)

            for thread in current_pool:
                thread.join()

        for env_name, env_id in results_dictionary.items():
            print(f"Started env {env_name} successfully with id {env_id}")

    def create_environment_executor(self, space_name, environment_name, duration_in_minutes: int, blueprint_name, description, owner, repository_name, collaborators: list[str] = [],
                                    blueprint_inputs: dict[str, str] = {}, out_results_dictionary={}):
        env_id = self.api_client.create_environment(space_name, environment_name, duration_in_minutes, blueprint_name,
                                                    description, owner, repository_name, collaborators, blueprint_inputs)
        out_results_dictionary[environment_name] = env_id


if __name__ == "__main__":
    args_dict = {arg.split("=")[0]: arg.split("=")[-1] for arg in sys.argv}
    deployer_app = TorqueDeployerApp(args_dict)
    deployer_app.main()
