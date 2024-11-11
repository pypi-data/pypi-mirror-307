import os

from .utils import error, warn, info, get_md5_from_comment, \
    cal_config_md5, line, get_real_comment, get_app_id_by_domain
from .read_config import read_yaml_config, write_yaml_config, add_before_comment

def check_basic_auth_groups(groups, filename):
    if not isinstance(groups, dict) and not isinstance(groups, list):
        error("unsupported file format for basic auth groups, file: {filename}")

    if isinstance(groups, dict):
        groups = [ groups ]

    for group in groups:
        if 'name' not in group:
            error("basic auth group name not found, file: {filename}")

        if 'users' not in group:
            error("basic auth group users not found, file: {filename}")

        label = group.get('label', '')
        group_name = group['name']
        if not isinstance(label, str):
            error(f"basic auth group label must be a string, file: {filename}, line: {line(label)}")

        users = group['users']
        for user in users:
            username = user.get("username", None)
            password = user.get("password", None)

            if not isinstance(username, str) or not username:
                error(f"invalid username in basic auth group {group_name}: {username}, file: {filename}, line: {line(user)}")

            if not isinstance(password, str) or not password:
                error(f"invalid password in basic auth group {group_name}: {password}, file: {filename}, line: {line(user)}")

    return True

def update_basic_auth_users(client, app_id, group_id, users):
    # get all users
    old_users = client.get_app_basic_auth_users_in_group(group_id, app_id=app_id)

    old_users_map = dict()
    for u in old_users:
        old_users_map[u['username']] = u

    for user in users:
        username = user['username']
        password = user['password']

        if username in old_users_map:
            # update
            try:
                info(f"updating basic auth user \"{username}\" to group, app id: {app_id}, group id: {group_id}")
                user_id = old_users_map[username]['id']
                client.put_app_basic_auth_user(user_id, group_id, username, password, app_id=app_id)
            except Exception as e:
                error(f"failed to update basic auth user, file: {filename}, line: {line(user)}", e)

            del(old_users_map[username])
        else:
            # add
            try:
                info(f"adding basic auth user \"{username}\" to group, app id: {app_id}, group id: {group_id}")
                client.new_app_basic_auth_user(group_id, username, password, app_id=app_id)
            except Exception as e:
                error(f"failed to add basic auth user, file: {filename}, line: {line(user)}", e)
            pass

    # delete
    for username, user in old_users_map.items():
        try:
            info(f"deleting basic auth user \"{username}\" from group, app id: {app_id}, group id: {group_id}")
            client.del_app_basic_auth_user(user["id"], group_id, app_id=app_id)
        except Exception as e:
            error(f"failed to delete basic auth user, file: {filename}, line: {line(user)}", e)


def basic_auth_group_changed(old_group, new_md5):
    if 'label' not in old_group:
        return True

    old_md5 = get_md5_from_comment(old_group['label'])
    if new_md5 and old_md5 == new_md5:
        return False

    return True

def process_basic_auth_groups(ctx):
    client = ctx['client']
    app_id = ctx['app_id']
    configs_path = ctx['configs_path']
    location = ctx.get('location', None)

    if not location:
        location = "basic_auth_groups"

    configs = read_yaml_config(configs_path, location)
    if configs is None:
        return

    # pre check
    info("Checking if basic auth groups are valid")
    for filename, groups in configs.items():
        check_basic_auth_groups(groups, filename)

    info("Checking if basic auth groups have changed")
    old_groups = client.get_all_app_basic_auth_user_groups(app_id)
    old_groups_map = dict()

    for g in old_groups:
        old_groups_map[g['name']] = g

    for filename, new_groups in configs.items():
        if isinstance(new_groups, dict):
            new_groups = [ new_groups ]
        for new_group in new_groups:
            # check if group exists
            name = new_group['name']
            md5 = cal_config_md5(new_group)

            if name not in old_groups_map:
                try:
                    info(f"adding basic auth group \"{name}\" to app, app id: {app_id}")
                    label = new_group.get('label', '')
                    label = f"{label}md5: {md5}, please do not modify."
                    group_id = client.new_app_basic_auth_user_group(name, label=label, app_id=app_id)
                    update_basic_auth_users(client, app_id, group_id, new_group['users'])
                except Exception as e:
                    error(f"failed to add basic auth group to app, file: {filename}, line: {line(new_group)}", e)

                # process next
                continue

            # group exists, check if group changed
            if basic_auth_group_changed(old_groups_map[name], md5):
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
                    update_basic_auth_users(client, app_id, group_id, new_group['users'])
                    info(f"updating basic auth group \"{name}\" to app, app id: {app_id}")
                    client.put_app_basic_auth_user_group(group_id, name, label=label, app_id=app_id)
                except Exception as e:
                    error(f"failed to update basic auth group to app, file: {filename}, line: {line(new_group)}", e)

            del(old_groups_map[name])

    # delete
    for name, group in old_groups_map.items():
        try:
            info(f"deleting basic auth group \"{name}\" from app, app id: {app_id}")
            client.del_app_basic_auth_user_group(group["id"], app_id=app_id)
        except Exception as e:
            error(f"failed to delete basic auth group to app, group id: {group['id']}, app id {app_id}", e)

def export_basic_auth_groups(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    domain = ctx['domain']
    configs_path = ctx['export_to_path']
    export_users = ctx.get('export_users', False)

    """
    Since passwords cannot be exported, not even users are exported by default

    Args:
        export_users (bool, optional): Whether to export users info. Defaults to False.
    """
    if ctx.get('app_not_found', False) is True:
        return

    app_id = ctx.get('app_id', None)
    if app_id is None:
        app_id = get_app_id_by_domain(client, partition_id, domain)
        if not app_id:
            warn(f"App not found, partition_id: {partition_id}, domain: {domain}")
            return

        ctx['app_id'] = app_id

    groups = client.get_all_app_basic_auth_user_groups(app_id)
    if not groups:
        info(f"No basic auth groups found for app_id: {app_id}")
        return

    formatted_groups = []
    for group in groups:
        formatted_group = {
            'name': group['name'],
            'label': group.get('label', ''),
            'users': []
        }

        # Get users for this group
        if export_users:
            password = ''
            if ctx['export_fake_info']:
                password = "********"

            users = client.get_app_basic_auth_users_in_group(group['id'], app_id=app_id)
            for user in users:
                formatted_user = {
                    'username': user['username'],
                    'password': password
                }
                formatted_user = add_before_comment(formatted_user, 'password',
                                                       "password: We don't export actual password for security reasons")
                formatted_group['users'].append(formatted_user)

        formatted_groups.append(formatted_group)

    export_path = os.path.join(configs_path, 'basic_auth_groups')

    try:
        for g in formatted_groups:
            group_name = g['name']
            write_yaml_config(export_path, f"{group_name}.yaml", [g])
            info(f"Basic auth group {group_name} exported successfully to basic_auth_groups/{group_name}.yaml")
        info(f"All basic auth groups exported successfully to basic_auth_groups/")
    except Exception as e:
        error(f"Failed to export basic auth groups to basic_auth_groups/", e)
