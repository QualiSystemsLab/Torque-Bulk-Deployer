"""
Torque Bulk Deployer app main application file
"""
import datetime
import json
import os
import sys
from sys import exit
from threading import Thread

import torque_bulk_deployer.consts as consts
from torque_bulk_deployer.torque_api_client import TorqueAPIClient


class TorqueDeployerApp:
    """
    Torque Bulk Deployer App main application class

    Attributes:
        auth_token      - saved Authorization token for the Torque API Session
        auth_usernaem   - saved username for the Torque API Session
        auth_password   - saved password for the Torque API Session
        api_client      - Instance of the Torque API Helper
    """
    auth_token:    str = ""
    auth_username: str = ""
    auth_password: str = ""
    api_client:    TorqueAPIClient = None

    def __init__(self, command_line_args=None):
        self.cli_args_dict = command_line_args

    def main(self):
        # print(args_dictionary)
        if "--help" in self.cli_args_dict or len(self.cli_args_dict) == 1:
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
        env_inputs = {env_input.split(":")[0]: env_input.split(":")[1] for env_input in env_inputs_str.split(";")}
        duration_minutes = int(self.cli_args_dict.get("--duration", 10))
        collaborators = self.cli_args_dict.get("--collaborators", "")
        if collaborators:
            collaborators = collaborators.split(";")

        env_id = self.api_client.create_environment(space_name, env_name, duration_minutes, blueprint_name, env_description, env_owner,
                                                    source_repo_name, collaborators, env_inputs)
        print(f"Started env {env_name} successfully with id {env_id}: https://portal.qtorque.io/{space_name}/sandboxes/{env_id}")

    def start_environments(self):
        if "--params_file" in self.cli_args_dict:
            common_args_list = self.read_common_args_from_file(self.cli_args_dict["--params_file"])
        else:
            common_args_list = [self.extract_cli_params()]

        env_creation_threads = []
        results_dictionary = {}
        for common_args in common_args_list:
            for owner in common_args["env_owners"]:
                env_name = f"{common_args['blueprint_name']} - {owner}"
                create_env_args = (common_args["space_name"], env_name, common_args["duration_minutes"], common_args["blueprint_name"],
                                   common_args["env_description"], owner, common_args["source_repo_name"], [], common_args["env_inputs"], results_dictionary)
                env_creation_threads.append(Thread(target=self.create_environment_executor, args=create_env_args))

            self._execute_threads_in_limited_pool(env_creation_threads)

            for env_name, env_id in results_dictionary.items():
                print(f"Started env {env_name} successfully with id {env_id}: https://portal.qtorque.io/{common_args['space_name']}/sandboxes/{env_id}")

    def _execute_threads_in_limited_pool(self, threads_list):
        joined_threads = 0
        while joined_threads < len(threads_list):
            current_pool = []
            for _ in range(5):
                if threads_list:
                    current_thread = threads_list.pop()
                    current_thread.start()
                    current_pool.append(current_thread)

            for thread in current_pool:
                thread.join()

    def extract_cli_params(self):
        """

        :return:
        """
        args = {"space_name":       self.cli_args_dict["--space_name"],
                "source_repo_name": self.cli_args_dict.get("--source_repo", "qtorque"),
                "blueprint_name":   self.cli_args_dict.get("--blueprint", "")}
        if args["source_repo_name"] == "qtorque":
            args["blueprint_name"] = "autogen_" + args["blueprint_name"]

        args["env_description"] = self.cli_args_dict.get("--description", "")
        env_inputs_str = self.cli_args_dict.get("--inputs", "")
        args["env_inputs"] = {env_input.split(":")[0]: env_input.split(":")[1].strip() for env_input in env_inputs_str.split(";")}
        args["duration_minutes"] = int(self.cli_args_dict.get("--duration", 10))

        args["env_owners"] = self.cli_args_dict["--owners"].split(";")
        return args

    def create_environment_executor(self, space_name, environment_name, duration_in_minutes: int, blueprint_name, description, owner, repository_name, collaborators: list[str] = [],
                                    blueprint_inputs: dict[str, str] = {}, out_results_dictionary={}):
        """
        :param space_name:
        :param environment_name:
        :param duration_in_minutes:
        :param blueprint_name:
        :param description:
        :param owner:
        :param repository_name:
        :param collaborators:
        :param blueprint_inputs:
        :param out_results_dictionary:
        """
        env_id = self.api_client.create_environment(space_name, environment_name, duration_in_minutes, blueprint_name,
                                                    description, owner, repository_name, collaborators, blueprint_inputs)
        out_results_dictionary[environment_name] = env_id

    def read_common_args_from_file(self, file_fullpath):
        args_list = []
        with open(file_fullpath, "r") as args_file:
            file_lines = args_file.readlines()
            for line in file_lines[1:]:
                line_args = line.split(",")
                current_line_args = {"space_name": line_args[0], "blueprint_name": line_args[1], "source_repo_name": line_args[2],
                                     "duration_minutes": int(line_args[3]), "env_owners": line_args[4].split(";")}
                if current_line_args["source_repo_name"] == "":
                    current_line_args["source_repo_name"] = "qtorque"
                    current_line_args["blueprint_name"] = "autogen_" + current_line_args["blueprint_name"]

                current_line_args["env_inputs"] = {env_input.split(":")[0]: env_input.split(":")[1].strip() for env_input in line_args[5].split(";")}
                current_line_args["env_description"] = ""
                args_list.append(current_line_args)

        return args_list


if __name__ == "__main__":
    args_dict = {arg.split("=")[0]: arg.split("=")[-1] for arg in sys.argv}
    deployer_app = TorqueDeployerApp(args_dict)
    deployer_app.main()
