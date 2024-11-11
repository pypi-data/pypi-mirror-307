import re

from .utils import error, warn, info, to_fake_name, line, to_real_name, extract_name

def replace_global_variables(client, content, partition_id):
    if not isinstance(content, str):
        raise Exception("bad content")

    variables = []
    pattern = r'\$or_global_user_variable_[a-zA-Z0-9_]+'
    variables = re.findall(pattern, content)

    variable_names = {}
    for var in variables:
        match = re.search(r'\$or_global_user_variable_(.*)', var)
        # should always match
        name = match.group(1)
        variable_names[var] = name

    global_variables = client.get_all_global_vars()
    if not isinstance(global_variables, list):
        global_variables = list()

    global_variable_names = {}
    for var in global_variables:
        global_variable_names[var['name']] = var['id']

    data = client.get_sync_to_all()
    ngx_sync_to_all = True
    if data and data.get('ngx', True) == False:
        ngx_sync_to_all = False

    for fake_name, name in variable_names.items():
        if name in global_variable_names:
            var_id = global_variable_names[name]
        else:
            # for compatibility with older versions of this tool
            real_name = to_real_name(name, partition_id, ngx_sync_to_all)
            if real_name in global_variable_names:
                var_id = global_variable_names[real_name]
            else:
                raise Exception(f"global variable not found in Edge Admin: {name}")

        content = content.replace(fake_name, f'$or-global-{var_id}')

    return content

def replace_global_variable_in_el(client, actions, filename, partition_id):
    if not isinstance(actions, list) and not isinstance(actions, dict):
        return

    if not isinstance(actions, list) and isinstance(actions, dict):
        new_actions = list()
        for k, v in actions.items():
            new_actions.append({k: v})
        actions = new_actions

    for action in actions:
        if not isinstance(action, dict) or 'user-code' not in action:
            continue

        el_value = ''
        user_code_data = action['user-code']
        if isinstance(user_code_data, dict) and 'el' in user_code_data:
            el_value = user_code_data['el']
        else:
            if user_code_data:
                error(f"bad action in page rule, file: {filename}, line: {line(user_code_data)}")
            else:
                error(f"bad action in page rule, file: {filename}, line: {line(user_code_data)}")

        try:
            user_code_data['el'] = replace_global_variables(client, el_value, partition_id)
        except Exception as e:
            error(f"failed to replace global variable in Edgelang, file: {filename}, line: {line(user_code_data)}", e)

def replace_global_variable_in_log_formats(client, log_formats, filename, partition_id):
    for name, fmt in log_formats.items():
        try:
            log_format = fmt['format']
            fmt['format'] = replace_global_variables(client, log_format, partition_id)
        except Exception as e:
            error(f"failed to replace global variable in access log format, file: {filename}, log format: {name}", e)

def restore_global_variable_names(client, content, partition_id):
    if not isinstance(content, str):
        raise Exception("Bad content")

    # Find all global variable IDs in the content
    pattern = r'\$or-global-[0-9]+'
    variables = re.findall(pattern, content)

    # Get all global variables
    global_variables = client.get_all_global_vars()
    if not isinstance(global_variables, list):
        global_variables = []

    # Create a mapping of variable IDs to names
    global_variable_ids = {var['id']: var['name'] for var in global_variables}

    # Replace each variable ID with its corresponding name
    for var in variables:
        match = re.search(r'\$or-global-(\d+)', var)
        if match:
            var_id = int(match.group(1))
            if var_id in global_variable_ids:
                var_name = global_variable_ids[var_id]
                # NAME_for_partition_ID to NAME
                var_name = extract_name(var_name)
                content = content.replace(var, f'$or_global_user_variable_{var_name}')
            else:
                warn(f"Global variable ID not found: {var_id}")

    return content

def restore_global_variable_names_in_el(client, actions, partition_id):
    if not isinstance(actions, list) and not isinstance(actions, dict):
        return

    if not isinstance(actions, list) and isinstance(actions, dict):
        new_actions = list()
        for k, v in actions.items():
            new_actions.append({k: v})
        actions = new_actions

    for action in actions:
        if not isinstance(action, dict) or 'user-code' not in action:
            continue

        user_code_data = action['user-code']
        if isinstance(user_code_data, dict) and 'el' in user_code_data:
            el_value = user_code_data['el']
            try:
                user_code_data['el'] = restore_global_variable_names(client, el_value, partition_id)
            except Exception as e:
                error(f"Failed to restore global variable names in Edgelang", e)

def restore_global_variable_names_in_log_formats(client, log_formats, partition_id):
    new_log_formats = list()
    for fmt in log_formats:
        name = fmt['name']
        try:
            log_format = fmt['format']
            new_fmt = {
                'name': fmt['name'],
                'format': restore_global_variable_names(client, log_format, partition_id),
                'default': fmt['default']
            }

            new_log_formats.append(new_fmt)
        except Exception as e:
            error(f"Failed to restore global variable names in access log format, log format: {name}", e)

    return new_log_formats
