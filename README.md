![quali](quali.png)

# Torque Bulk Deployer
Torque Bulk Deployer is a lightweight, python-based .exe CLI tool for deploying Torque Blueprints in bulk for several owners at once. 

## **Installation**
No installation needed - just download the .exe file and run it from Windows Command Line/PowerShell. 

If you want it to be available by default in any Command Line session, place it in C:\Windows\System32 and C:\Windows\SysWOW64  

## **Basic Usage**

Execute **torque_bulk_deployer.exe --help** or without any arguments to get this help message:

```
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
```

in order to execute any command, you havae to provide Torque authentication info, this can be done in any of the following ways:
1. API Authorization Token: provide a pre-provisioned Torque API Authorization token using --auth_token=THISISNOTAREALTOKEN, obtained by sending POST to https://portal.qtorque.io/api/accounts/login with body of `{"email":<user_email>, "password":<user_password>}
    
    Note that you can obtain a long-term token by POST to https://portal.qtorque.io/api/token/longtoken with a header that includes a currently active short-term token: headers: { "Authorization": "Bearer <token_data>" }
2. Username & Password: provide your username and password information using --username=<user_email> and --password=<user_password>

    when using Username & Password, you also need to specify the Torque account name using --account=<account_name>
3. Config File: save the information for either option 1 or 2 in a .json file and provide the path to it using --config_file=<path_to_json>

    example of such a JSON config file:
    ```JSON
    {
        "auth_token": "this_is_not_a_real_auth_token",
        "username": "john.d@quali.com",
        "password": "JohnDsPasswordIsNot123",
        "account": "demo"
    }
    ```

## **Specific Usage samples**

### **Get a list of Blueprints in a specifc space:**
```powershell
torque_bulk_deployer.exe <authentication info> get_blueprints --space_name=<space_name> --published_only=true|false
```

### **Create a single Environment from a Blueprint**
```powershell
torque_bulk_deployer.exe <authentication info> start_environment --space_name=<space_name> --blueprint=<blueprint_name> --source_repo=<blueprint_source_repo> --owner=<owner_email> --inputs=<environmeent_input_values> --duration=<duration_in_minutes>
```

### **Create multiple Environments from one or more Blueprints**
```powershell
torque_bulk_deployer.exe <authentication info> start_environments --params_file=<my_csv_file_path> --stagger_duration=<stagger_time_in_seconds>
```

when providing a params file for a bulk deployment request, it needs to be a .csv file with the following header structure:

| Space         | Blueprint | Repository   | Duration (Minutes)   | Owners                   | Inputs     | 
| -----         | --------- | ----------   | ------------------   | ------                   | ------     | 
| bp_space_name | bp_name   | bp_repo_name | env_duration_minutes | owner_emails_;_separated | env_inputs | 

**Note:** The first line of the CSV file is considered a headers line and is ignored.

```
Options:
    --stagger_duration=<N>                      if specified, there will be an N second delay between launching each environment 
```

## Troubleshooting and Help

For questions, bug reports or feature requests, please refer to the [Issue Tracker]. Also, make sure you check out our [Issue Template](.github/issue_template.md).

## Contributing


All your contributions are welcomed and encouraged.  We've compiled detailed information about:

* [Contributing](.github/contributing.md)
* [Creating Pull Requests](.github/pull_request_template.md)


## License
[Apache License 2.0](https://github.com/QualiSystems/shellfoundry/blob/master/LICENSE)
