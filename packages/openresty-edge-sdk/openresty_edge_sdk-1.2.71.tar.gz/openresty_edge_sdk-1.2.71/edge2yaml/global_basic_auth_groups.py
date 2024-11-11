import os

from .utils import error, warn, info, get_md5_from_comment, \
    cal_config_md5, line, get_real_comment
from .read_config import read_yaml_config, write_yaml_config, add_before_comment

def check_global_basic_auth_groups(groups, filename):
    if not isinstance(groups, list):
        error(f"Unsupported file format for global basic auth groups, file: {filename}")

    for group in groups:
        if 'name' not in group:
            error(f"Global basic auth group name not found, file: {filename}")

        if 'users' not in group:
            error(f"Global basic auth group users not found, file: {filename}")

        label = group.get('label', '')
        group_name = group['name']
        if not isinstance(label, str):
            error(f"Global basic auth group label must be a string, file: {filename}, line: {line(label)}")

        users = group['users']
        for user in users:
            username = user.get("username", None)
            password = user.get("password", None)

            if not isinstance(username, str) or not username:
                error(f"Invalid username in global basic auth group {group_name}: {username}, file: {filename}, line: {line(user)}")

            if not isinstance(password, str) or not password:
                error(f"Invalid password in global basic auth group {group_name}: {password}, file: {filename}, line: {line(user)}")

    return True

def update_global_basic_auth_users(client, group_id, users):
    old_users = client.get_global_basic_auth_users_in_group(group_id)

    old_users_map = {u['username']: u for u in old_users}

    for user in users:
        username = user['username']
        password = user['password']

        if username in old_users_map:
            try:
                info(f"Updating global basic auth user \"{username}\" in group, group id: {group_id}")
                user_id = old_users_map[username]['id']
                client.put_global_basic_auth_user(user_id, group_id, username, password)
            except Exception as e:
                error(f"Failed to update global basic auth user, username: {username}", e)

            del old_users_map[username]
        else:
            try:
                info(f"Adding global basic auth user \"{username}\" to group, group id: {group_id}")
                client.new_global_basic_auth_user(group_id, username, password)
            except Exception as e:
                error(f"Failed to add global basic auth user, username: {username}", e)

    for username, user in old_users_map.items():
        try:
            info(f"Deleting global basic auth user \"{username}\" from group, group id: {group_id}")
            client.del_global_basic_auth_user(user["id"], group_id)
        except Exception as e:
            error(f"Failed to delete global basic auth user, username: {username}", e)

def global_basic_auth_group_changed(old_group, new_md5):
    if 'label' not in old_group:
        return True

    old_md5 = get_md5_from_comment(old_group['label'])
    if new_md5 and old_md5 == new_md5:
        return False

    return True

def process_global_basic_auth_groups(ctx):
    client = ctx['client']
    configs_path = ctx['configs_path']
    location = ctx.get('location', None)

    if not location:
        location = "global_basic_auth_groups"

    configs = read_yaml_config(configs_path, location)
    if configs is None:
        return

    info("Checking if global basic auth groups are valid")
    for filename, groups in configs.items():
        check_global_basic_auth_groups(groups, filename)

    info("Checking if global basic auth groups have changed")
    old_groups = client.get_all_global_basic_auth_user_groups()
    old_groups_map = {g['name']: g for g in old_groups}

    for filename, new_groups in configs.items():
        for new_group in new_groups:
            name = new_group['name']
            md5 = cal_config_md5(new_group)

            if name not in old_groups_map:
                try:
                    info(f"Adding global basic auth group \"{name}\"")
                    label = new_group.get('label', '')
                    label = f"{label}md5: {md5}, please do not modify."
                    group_id = client.new_global_basic_auth_user_group(name, label=label)
                    update_global_basic_auth_users(client, group_id, new_group['users'])
                except Exception as e:
                    error(f"Failed to add global basic auth group, file: {filename}, line: {line(new_group)}", e)
                continue

            if global_basic_auth_group_changed(old_groups_map[name], md5):
                label = new_group.get('label', '')
                if label:
                    label = f"{label}md5: {md5}, please do not modify."
                else:
                    label = old_groups_map[name].get('label', '')
                    if label:
                        label = get_real_comment(label)
                        label = f"{label}md5: {md5}, please do not modify."
                    else:
                        label = f"md5: {md5}, please do not modify."

                try:
                    group_id = old_groups_map[name]['id']
                    update_global_basic_auth_users(client, group_id, new_group['users'])
                    info(f"Updating global basic auth group \"{name}\"")
                    client.put_global_basic_auth_user_group(group_id, name, label=label)
                except Exception as e:
                    error(f"Failed to update global basic auth group, file: {filename}, line: {line(new_group)}", e)

            del old_groups_map[name]

    # since this is a global configuration,
    # we will not perform deletion operations in order to maintain compatibility with multiple local configurations.
    # for name, group in old_groups_map.items():
    #     try:
    #         info(f"Deleting global basic auth group \"{name}\"")
    #         client.del_global_basic_auth_user_group(group["id"])
    #     except Exception as e:
    #         error(f"Failed to delete global basic auth group, group id: {group['id']}", e)

def export_global_basic_auth_groups(ctx):
    client = ctx['client']
    configs_path = ctx['export_to_path']
    export_users = ctx.get('export_users', False)

    groups = client.get_all_global_basic_auth_user_groups()
    if not groups:
        info("No global basic auth groups found")
        return

    formatted_groups = []
    for group in groups:
        formatted_group = {
            'name': group['name'],
            'label': get_real_comment(group.get('label', '')),
            'users': []
        }

        if export_users:
            password = ''
            if ctx['export_fake_info']:
                password = "********"

            users = client.get_global_basic_auth_users_in_group(group['id'])
            for user in users:
                formatted_user = {
                    'username': user['username'],
                    'password': password
                }
                formatted_user = add_before_comment(formatted_user, 'username',
                                                       "password: We don't export actual password for security reasons")
                formatted_group['users'].append(formatted_user)

        formatted_groups.append(formatted_group)

    if not export_users:
        warn("global basic auth users will not be exported")

    export_path = os.path.join(configs_path, 'global_basic_auth_groups')

    try:
        write_yaml_config(export_path, "global_basic_auth_groups.yaml", formatted_groups)
        info("Global basic auth groups exported successfully to global_basic_auth_groups/global_basic_auth_groups.yaml")
    except Exception as e:
        error("Failed to export global basic auth groups to global_basic_auth_groups/global_basic_auth_groups.yaml", e)

def cleanup_global_basic_auth_groups(ctx):
    pass
    # since this is a global configuration,
    # we will not perform deletion operations in order to maintain compatibility with multiple local configurations.
    # client = ctx['client']

    # groups = client.get_all_global_basic_auth_user_groups()

    # for group in groups:
    #     try:
    #         info(f"Removing global basic auth group \"{group['name']}\"")
    #         client.del_global_basic_auth_user_group(group["id"])
    #     except Exception as e:
    #         error(f"Failed to remove global basic auth group, group id: {group['id']}", e)
