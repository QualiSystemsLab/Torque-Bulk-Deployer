TORQUE_API_BASE = "https://portal.qtorque.io/api"

HELP_TEXT = """\
Usage: torque_bulk_deployer [OPTIONS] Command [COMMAND OPTIONS]

Options:
    --help                      show this message
    --config_file=<file_path>   use a config file from a different directory
    --auth_token=<token>        use a different token than the config file

Commands:
get_blueprints      Show all Blueprints info
start_environment   Start a Torque environment
start_environmnets  Start multiple Torque environments

"""