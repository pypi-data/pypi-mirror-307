import os

from jinja2 import Template

from .utils import error, warn, info, line
from .read_config import read_yaml_config, write_yaml_config
from .edge_email import send_email

login_types = {
    'Normal': 'normal',
    'LDAP': 'ldap',
    'OpenIDC': 'oidc',
    'none': 'none',
}

login_type_names = {
    'normal': 'Normal',
    'ldap': 'LDAP',
    'oidc': 'OpenIDC',
    'none': 'none',
}

def render_email(template, username, password, user_id, user_group, user_group_id):
    tm = Template(template)
    return tm.render(username=username, password=password,
                     user_id=user_id, user_group=user_group,
                     user_group_id=user_group_id)

def send_email_to_user(email_configs, user, user_id, group_names, group_ids):
    subject = email_configs['new_user_email_template']['subject']
    content = email_configs['new_user_email_template']['content']
    content = render_email(content, user['username'], user['password'],
                            user_id, ",".join(group_names), ",".join(map(str, group_ids)))
    info("sending email to user: " + user['username'] + ", email: " + user['email'])
    ok = send_email(email_configs, user['email'], subject, content)
    if not ok:
        error("send email to " + user['email'] + " failed")

def process_users(ctx):
    client = ctx['client']
    configs_path = ctx['users_config_path']
    email_configs = ctx['email_configs']

    if configs_path is None:
        return True

    configs = read_yaml_config(configs_path)
    if configs is None:
        return True

    users = list()
    user_groups = None
    sorted_filenames = sorted(configs.keys())
    # check users and format users
    for filename in sorted_filenames:
        config = configs[filename]
        if not isinstance(config, dict):
            error(f"unsupported file format for users, file: {filename}")

        if 'users' not in config:
            error(f"users not found in file: {filename}")

        def_change_pwd_on_login = config.get('change_pwd_on_login', False)
        def_login_type = config.get('login_type', 'Normal')
        def_password = config.get('password', None)
        def_allow_login = config.get('allow_login', True)
        def_group_name = config.get('group', None)
        def_send_email_to_existing_user = config.get('send_email_to_existing_user', False)
        def_send_email_to_new_user = config.get('send_email_to_new_user', False)

        for user in config['users']:
            if not isinstance(user, dict):
                error(f"unsupported file format for users, file: {filename}, line: {line(user)}")

            if 'username' not in user:
                error(f"username not found in user, file: {filename}, line: {line(user)}")

            login_type = user.get('login_type', None)
            if login_type is None:
                warn(f"Login type not found in user, file: {filename}, line: {line(user)}, using default login type: {def_login_type}")
                login_type = [ def_login_type ]

            if not isinstance(login_type, list):
                login_type = [ login_type ]

            for typ in login_type:
                if typ not in login_types:
                    error(f"unsupported login type: {typ}, file: {filename}, line: {line(user)}")

            password = user.get('password', def_password)
            if not isinstance(password, str):
                error(f"password must be a string, file: {filename}, line: {line(user)}")

            allow_login = user.get('allow_login', def_allow_login)
            if not isinstance(allow_login, bool):
                error(f"allow_login must be a boolean, file: {filename}, line: {line(user)}")

            if allow_login is False:
                login_type = [ 'none' ]

            change_pwd_on_login = user.get('change_pwd_on_login', def_change_pwd_on_login)
            if not isinstance(change_pwd_on_login, bool):
                error(f"change_pwd_on_login must be a boolean, file: {filename}, line: {line(user)}")

            group_name = user.get('group', def_group_name)
            if not isinstance(group_name, str) and not isinstance(group_name, list):
                error(f"group must be a string, file: {filename}, line: {line(user)}")

            if isinstance(group_name, str):
                group_names = [ group_name ]

            # check if user group exists
            if user_groups is None:
                groups = client.get_all_user_groups()
                if groups is None:
                    error(f"failed to get user groups")

                user_groups = dict()
                for g in groups:
                    # g['permission'] = None
                    name = g.get('group_name')
                    user_groups[name] = g['id']

            for group in group_names:
                if group not in user_groups:
                    error(f"user group not found: {group}, file: {filename}, line: {line(user)}")

            if 'email' not in user and user.get('send_email_to_new_user', False) == True:
                error(f"email not found in user, file: {filename}, line: {line(user)}")

            real_login_types = [ login_types[typ] for typ in login_type ]
            real_gids = [ user_groups[group] for group in group_names ]

            users.append({
                'username': user['username'],
                'password': password,
                'requires_password_change': change_pwd_on_login,
                'login_type': real_login_types,
                'gid': real_gids,
                'group_names': group_names,
                'email': user.get('email', None),
                'send_email_to_existing_user': user.get('send_email_to_existing_user', def_send_email_to_existing_user),
                'send_email_to_new_user': user.get('send_email_to_new_user', def_send_email_to_new_user),
            })

    for user in users:
        # check if user exists
        data = client.search_global_user(user['username'])
        user_id = data.get('id', None)

        if isinstance(user_id, int):
            # check next users
            warn(f"User {user['username']} already exists, id: {user_id}")

            if 'email' in user and user.get('send_email_to_existing_user', None) == True:
                if email_configs is None:
                    warn(f"unable to send email to {user['email']}, because the sender's email config was not found")
                else:
                    send_email_to_user(email_configs, user, user_id, user['group_names'], user['gid'])

            continue

        # new user
        data = client.add_global_user(user['username'], user['password'],
                               gid=user['gid'],
                               login_type=user['login_type'],
                               requires_password_change=user['requires_password_change'])

        user_id = data.get('id', None)
        if not isinstance(user_id, int):
            error(f"failed to add user: {user['username']}")

        info("added user: " + user['username'] + ", id: " + str(user_id) + ", user groups: " + ",".join(user['group_names']))

        # send email
        if 'email' in user and user.get('send_email_to_new_user', False) == True:
            if email_configs is None:
                warn(f"unable to send email to {user['email']}, because the sender's email config was not found")
            else:
                send_email_to_user(email_configs, user, user_id, user['group_names'], user_groups)

def export_users_and_groups(ctx):
    client = ctx['client']
    configs_path = ctx['export_to_path']
    export_users = ctx.get('export_users', False)

    # Export user groups and their users
    info("Exporting user groups and users...")

    if export_users is False:
        warn("User passwords will not be exported")

    export_path = os.path.join(configs_path, "users")

    user_groups = client.get_all_user_groups()
    groups_map = dict()
    for group in user_groups:
        group_name = group['group_name']
        group_id = group['id']
        groups_map[group_id] = group_name

    users = client.get_all_global_users(detail=True)
    group_users = dict()
    for user in users:
        # for gid in user['gid']:
        # just add to the first group
        gid = user['gid'][0]
        group_name = groups_map.get(gid)
        if group_name not in group_users:
            group_users[group_name] = list()

        group_users[group_name].append(user)

    for group in user_groups:
        group_name = group['group_name']
        group_id = group['id']

        export_data = {
            'group': group_name,
            'users': []
        }

        if export_users is True:
            users = group_users.get(group_name, list())
            for user in users:
                # user_details = client.get_global_user(user['id'])
                formatted_user = {
                    'username': user['username'],
                    'email': user.get('email', None),
                    'group': [ groups_map.get(gid) for gid in user['gid'] ],
                    'login_type': [ login_type_names[name] for name in user.get('login_type', ['normal']) ],
                    'allow_login': user.get('login_type', ['normal'])[0] != 'none',
                    'change_pwd_on_login': user.get('requires_password_change', False),
                    'send_email_to_existing_user': False,  # Default value, adjust as needed
                    'send_email_to_new_user': False,  # Default value, adjust as needed
                }
                export_data['users'].append(formatted_user)

        # Write to YAML file
        try:
            write_yaml_config(export_path, f"{group_name}.yaml", export_data)
            if export_users is True:
                info(f"User group '{group_name}' and its users exported successfully to users/{group_name}.yaml")
            else:
                info(f"User group '{group_name}' exported successfully to users/{group_name}.yaml")
        except Exception as e:
            error(f"Failed to export user group '{group_name}' and its users to users/{group_name}.yaml", e)

    info(f"All user groups and users exported successfully to users/")
