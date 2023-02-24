TORQUE_API_BASE = "https://portal.qtorque.io/api"

HELP_TEXT = """\
Usage: torque_bulk_deployer [OPTIONS] Command [COMMAND OPTIONS]

Options:
    --help                      show this message / show Command help
    --config_file=<file_path>   use a config file from a different directory
    --auth_token=<token>        use a pre-existing auth_token (if using this option, no need to provider username, password and account_name)
    --username=<user_email>     username of user account to use (e-mail address)
    --password=<password>       password of user account to use 
    --account                   Torque account name (if user has access to more than 1 account)

note: config_params auth_token, username, password, account are optional if JSON file containing these values is used

Commands:
get_blueprints      Show all Blueprints info
start_environment   Start a Torque environment
start_environmnets  Start multiple Torque environments

"""

GET_BLUEPRINTS_HELP = """\
Displays a YAML formatted list of Blueprints in a given Torque Space

Usage: torque_bulk_deployer [OPTIONS] get_blueprints [COMMAND ARGS]

for list of [OPTIONS], run torque_bulk_deployer --help

Mandatory Command Arguments:    
    --space_name=<space_name>   name of Torque space to query

Optional Command Arguments:
    --help                      show this message and exit
    --published_only=true|false show only published Blueprints (default = false)
"""

START_ENVIRONMENT_HELP = """\
Creates a new Torque Environment from a blueprint

Usage: torque_bulk_deployer [OPTIONS] start_environment [COMMAND ARGS]

for list of [OPTIONS], run torque_bulk_deployer --help

Mandatory Command Arguments:
    --space_name=<space_name>       name of Torque space in which the environment will be created
    --blueprint=<bp_name>           name of the Blueprint to use
    --owner=<owner_email>           username (e-mail address) of the new environment's owner
    --inputs=<inputs_list>          Key-Value list of input names and values for the environment (e.g. a:1,b:2)
    --duration=<duration_in_mins>   Duration of the environment in minutes

Optional Command Arguments:
    --help                          show this message and exit
    --source_repo=<repo_name>       logical name of the source control repository the Blueprint is from (omit for Blueprints stored in Torque)
    --environment_name=<env_name>   name of the new environment that will be created
    --description=<env_desc>        description of the new environment that will be created
    --space_name=<space_name>       name of Torque space to query
"""

START_ENVIRONMENTS_HELP = """\
Creates multiple new Torque Environments from a blueprint

Usage: torque_bulk_deployer [OPTIONS] start_environments [COMMAND ARGS]

for list of [OPTIONS], run torque_bulk_deployer --help

Mandatory Command Arguments:
    --params_file=<path_to_file>    CSV file with bulk request parameters
    OR
    --space_name=<space_name>       name of Torque space in which the environment will be created
    --blueprint=<bp_name>           name of the Blueprint to use
    --owners=<owner_emails_list>    list of usernames (e-mail address) of the new environments owners, separated by semicolon (e.g. john.d@example.com;jane.d@example.com)
    --inputs=<inputs_list>          Key-Value list of input names and values for the environment (e.g. a:1,b:2)
    --duration=<duration_in_mins>   Duration of the environment in minutes

Optional Command Arguments:
    --help                          show this message and exit
    --source_repo=<repo_name>       logical name of the source control repository the Blueprint is from (omit for Blueprints stored in Torque)
    --description=<env_desc>        description of the new environment that will be created
    --space_name=<space_name>       name of Torque space to query
"""