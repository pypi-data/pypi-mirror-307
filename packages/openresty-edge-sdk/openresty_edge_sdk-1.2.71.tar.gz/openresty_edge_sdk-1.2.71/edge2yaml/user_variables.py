import os
import re

from .utils import error, warn, info, get_app_id_by_domain, release_changes, \
    clear_changes, line
from .read_config import read_yaml_config, write_yaml_config

def replace_variables(client, content):
    if not isinstance(content, str):
        raise Exception("bad content")

    variables = []
    pattern = r'\$or_user_variable_[a-zA-Z0-9_]+'
    variables = re.findall(pattern, content)

    variable_names = {}
    for var in variables:
        match = re.search(r'\$or_user_variable_(.*)', var)
        # should always match
        name = match.group(1)
        var_name =name
        variable_names[var] = var_name

    user_variables = client.get_all_user_vars()
    if not isinstance(user_variables, list):
        user_variables = list()

    user_variable_names = {}
    for var in user_variables:
        user_variable_names[var['name']] = var['id']

    for fake_name, real_name in variable_names.items():
        if real_name not in user_variable_names:
            raise Exception(f"user variable not found: {real_name}")

        var_id = user_variable_names[real_name]

        content = content.replace(fake_name, f'$or-{var_id}')

    return content

def restore_variable_names(client, content):
    if not isinstance(content, str):
        raise Exception("Bad content")

    # Find all global variable IDs in the content
    pattern = r'\$or-[0-9]+'
    content_variables = re.findall(pattern, content)

    # Get all global variables
    variables = client.get_all_user_vars()
    if not isinstance(variables, list):
        variables = []

    # Create a mapping of variable IDs to names
    variable_ids = {var['id']: var['name'] for var in variables}

    # Replace each variable ID with its corresponding name
    for var in content_variables:
        match = re.search(r'\$or-(\d+)', var)
        if match:
            var_id = int(match.group(1))
            if var_id in variable_ids:
                var_name = variable_ids[var_id]
                real_name = var_name
                if real_name is None:
                    error(f"Variable {var_name}(id: {var_id}) is not for the partition {partition_id}")

                content = content.replace(var, f'$or_user_variable_{real_name}')
            else:
                warn(f"Global variable ID not found: {var_id}")

    return content

def check_user_variables(variables, filename):
    if not isinstance(variables, list):
        error(f"Unsupported user variables file format, file: {filename}")

    valid_types = ['string', 'enum', 'num', 'int', 'bool']

    names = dict()
    for var in variables:
        if not isinstance(var, dict):
            error(f"Each user variable must be a dictionary, file: {filename}, line: {line(var)}")

        if 'name' not in var:
            error(f"Missing 'name' in user variable, file: {filename}, line: {line(var)}")

        if 'type' not in var:
            error(f"Missing 'type' in user variable {var['name']}, file: {filename}, line: {line(var)}")

        if var['type'] not in valid_types:
            error(f"Invalid type '{var['type']}' for user variable {var['name']}, file: {filename}, line: {line(var)}")

        if 'default' not in var:
            error(f"Missing 'default' in user variable {var['name']}, file: {filename}, line: {line(var)}")

        if var['type'] == 'enum':
            if 'values' not in var or not isinstance(var['values'], list):
                error(f"Missing or invalid 'values' for enum variable {var['name']}, file: {filename}, line: {line(var)}")
            if var['default'] not in var['values']:
                error(f"Default value not in enum values for variable {var['name']}, file: {filename}, line: {line(var)}")

        if var['type'] == 'num':
            try:
                float(var['default'])
            except ValueError:
                error(f"Invalid default value for num variable {var['name']}, file: {filename}, line: {line(var)}")

        if var['type'] == 'int':
            try:
                int(var['default'])
            except ValueError:
                error(f"Invalid default value for int variable {var['name']}, file: {filename}, line: {line(var)}")

        if var['type'] == 'bool':
            if var['default'].lower() not in ['true', 'false']:
                error(f"Invalid default value for bool variable {var['name']}, file: {filename}, line: {line(var)}")

        if var['name'] in names:
            error(f"Duplicate name in user variable {var['name']}, file: {filename}, line: {line(var)}")

        names[var['name']] = True

    return True

def is_change_user_variable(new_var, old_var):
    if (new_var['name'] != old_var['name'] or
            new_var['type'] != old_var['type'] or
            new_var['default'] != old_var['default']):
        return True

    if new_var['type'] == 'enum' and new_var.get('values') != old_var.get('values'):
        return True

    return False

def process_user_variables(ctx):
    client = ctx['client']
    app_id = ctx['app_id']
    configs_path = ctx['configs_path']
    location = ctx.get('location', None)
    staging_release = ctx.get('staging_release', None)

    if not location:
        location = "user_variables"

    configs = read_yaml_config(configs_path, location)
    if configs is None:
        return

    info("Checking if user variables are valid")
    for filename, variables in configs.items():
        check_user_variables(variables, filename)

    client.use_app(app_id)
    old_variables = client.get_all_user_vars()

    old_variables_dict = {var['name']: var for var in old_variables}

    info("Checking if user variables have changed")
    new_variables_dict = {}
    sorted_configs = sorted(configs.keys())

    for filename in sorted_configs:
        variables = configs[filename]
        for var in variables:
            new_variables_dict[var['name']] = True

            if var['name'] in old_variables_dict:
                old_var = old_variables_dict[var['name']]
                if is_change_user_variable(var, old_var):
                    try:
                        info(f"Updating user variable \"{var['name']}\", app id: {app_id}")
                        client.put_user_var(
                            var_id=old_var['id'],
                            name=var['name'],
                            var_type=var['type'],
                            default=var['default'],
                            values=var.get('values')
                        )
                    except Exception as e:
                        clear_changes(client, app_id)
                        error(f"Failed to update user variable, file: {filename}, line: {line(var)}", e)
            else:
                try:
                    info(f"Adding user variable \"{var['name']}\" to app, app id: {app_id}")
                    client.new_user_var(
                        name=var['name'],
                        var_type=var['type'],
                        default=var['default'],
                        values=var.get('values')
                    )
                except Exception as e:
                    clear_changes(client, app_id)
                    error(f"Failed to add user variable to app, file: {filename}, line: {line(var)}", e)

    for var_name, var in old_variables_dict.items():
        if var_name not in new_variables_dict:
            try:
                info(f"Removing user variable \"{var_name}\" from app, app id: {app_id}")
                client.del_user_var(var['id'])
            except Exception as e:
                clear_changes(client, app_id)
                error(f"Failed to remove user variable from app, app id: {app_id}, variable id: {var['id']}", e)

    release_changes(client, app_id, staging_release=staging_release)

def cleanup_user_variables(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    domain = ctx['domain']
    staging_release = ctx.get('staging_release', None)

    app_id = get_app_id_by_domain(client, partition_id, domain)
    if not app_id:
        error(f"App not found, app id: {app_id}, domain: {domain}")

    client.use_app(app_id)
    user_variables = client.get_all_user_vars()

    for var in user_variables:
        try:
            info(f"Removing user variable \"{var['name']}\" from app, app id: {app_id}")
            client.del_user_var(var['id'])
        except Exception as e:
            clear_changes(client, app_id)
            error(f"Failed to remove user variable from app, app id: {app_id}, variable id: {var['id']}", e)

    release_changes(client, app_id, staging_release=staging_release)

def export_user_variables(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    domain = ctx['domain']
    configs_path = ctx['export_to_path']

    if ctx.get('app_not_found', False) is True:
        return

    app_id = ctx.get('app_id', None)
    if app_id is None:
        app_id = get_app_id_by_domain(client, partition_id, domain)
        if not app_id:
            warn(f"App not found, partition_id: {partition_id}, domain: {domain}")
            return

        ctx['app_id'] = app_id

    client.use_app(app_id)
    user_variables = client.get_all_user_vars()

    if not user_variables:
        info(f"No user variables found for app_id: {app_id}")
        return

    formatted_variables = []
    for var in user_variables:
        formatted_var = {
            'name': var['name'],
            'type': var['type'],
            'default': var['default']
        }
        if var['type'] == 'enum':
            formatted_var['values'] = var['values']
        formatted_variables.append(formatted_var)

    export_path = os.path.join(configs_path, "user_variables")

    try:
        write_yaml_config(export_path, "user_variables.yaml", formatted_variables)
        info(f"User variables exported successfully to user_variables/user_variables.yaml")
    except Exception as e:
        error(f"Failed to export user variables to user_variables/user_variables.yaml", e)
