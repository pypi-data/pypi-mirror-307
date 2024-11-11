import os

from .utils import error, warn, info, get_app_id_by_domain, line, check_type, \
    get_md5_from_comment, cal_config_md5, clear_changes, release_changes, get_real_comment
from .read_config import read_yaml_config, write_yaml_config, format_yaml_content
from .global_variables import restore_global_variable_names, replace_global_variables
from .global_page_templates import id_to_name as page_template_id_to_name, name_to_id as page_template_name_to_id
from .user_variables import restore_variable_names, replace_variables

def delete_page_rules(client, app_id):
    client.use_app(app_id)
    info(f"removing all page rules in app, app id: {app_id}")
    rules = client.get_all_rules(app_id)
    for rule in rules:
        if 'id' in rule:
            info(f"removing page rule from app, app id: {app_id}, page rule id: {rule['id']}")
            client.del_rule(rule['id'])

def build_names_map(ctx, key, func, id_to_str=False, args={}):
    names_map = ctx.get(key, dict())
    if not names_map:
        records = func(**args)
        for record in records:
            record_id = record['id']
            if id_to_str:
                record_id = str(record['id'])

            names_map[record['name']] = record_id

        ctx[key] = names_map

    return names_map

def build_static_file_map(ctx, key):
    client = ctx['client']

    file_map = ctx.get(key, dict())
    if not file_map:
        paths_to_check = [""]
        while paths_to_check:
            current_path = paths_to_check.pop(0)
            files = client.get_all_static_files(path=current_path)
            for file in files:
                file_map[file['path']] = file['id']
                if file['type'] == 'dir':
                    paths_to_check.append(file['path'])

        ctx[key] = file_map

    return file_map

def check_conditions(ctx, filename, rule):
    if 'conditions' not in rule:
        return True

    client = ctx['client']

    for condition in rule['conditions']:
        if 'user_var' in condition:
            user_variable_map = build_names_map(ctx, "user_variable_map", client.get_all_user_vars)
            if condition['user_var'] not in user_variable_map:
                error(f"unknown user variable: {condition['user_var']}, filename: {filename}, line: {line(condition)}")

        if 'global_var' in condition:
            global_variable_map = build_names_map(ctx, "global_variable_map", client.get_all_global_vars)
            if condition['global_var'] not in global_variable_map:
                error(f"unknown global user variable: {condition['global_var']}, filename: {filename}, line: {line(condition)}")

        if 'vals' in condition:
            if not isinstance(condition['vals'], list):
                error(f"condition vals must be a list, filename: {filename}, line: {line(condition)}")

            for val in condition['vals']:
                if not isinstance(val, str) and not isinstance(val, dict):
                    error(f"condition vals must be str or dict, filename: {filename}, line: {line(condition)}")

                if isinstance(val, dict) and ('val' not in val or 'type' not in val):
                    error(f"condition val must have val and type, filename: {filename}, line: {line(condition)}")

                if isinstance(val, dict):
                    if val['type'] == "app-ip-list":
                        app_ip_list_map = build_names_map(ctx, "app_ip_list_map", client.get_all_ip_lists, True)
                        # check if app ip list exists
                        if val['val'] not in app_ip_list_map:
                            error(f"app ip list {val['val']} not found, filename: {filename}, line: {line(condition)}")

                    if val['type'] == "ip-list":
                        global_ip_list_map = build_names_map(ctx, "global_ip_list_map", client.get_all_global_ip_lists, True)
                        # check if global ip list exists
                        if val['val'] not in global_ip_list_map:
                            error(f"global ip list {val['val']} not found, filename: {filename}, line: {line(condition)}")


def check_actions(ctx, filename, rule):
    if 'actions' not in rule:
        return True

    if isinstance(rule['actions'], dict):
        new_actions = list()
        for k, v in rule['actions'].items():
            new_actions.append({k: v})
        rule['actions'] = new_actions

    client = ctx['client']
    valid_var_types = [ "app", "global" ]

    for action in rule['actions']:
        if 'set-var' in action:
            if 'var_type' not in action['set-var'] or 'var_name' not in action['set-var']:
                error(f"set-var must have var_type and var_name, filename: {filename}, line: {line(action)}")

            if action['set-var']['var_type'] not in valid_var_types:
                error(f"unknown user variable type: {action['set-var']['var_type']}, filename: {filename}, line: {line(action)}")

            if action['set-var']['var_type'] == 'global':
                global_user_variable_map = build_names_map(ctx, "global_user_variable_map", client.get_all_global_vars)
                if action['set-var']['var_name'] not in global_user_variable_map:
                    error(f"unknown global user variable: {action['set-var']['var_name']}, filename: {filename}, line: {line(action)}")

            if action['set-var']['var_type'] == 'http':
                user_variable_map = build_names_map(ctx, "user_variable_map", client.get_all_user_vars)
                if action['set-var']['var_name'] not in user_variable_map:
                    error(f"unknown user variable: {action['set-var']['var_name']}, filename: {filename}, line: {line(action)}")

        if 'block-req' in action or 'limit-req-rate' in action:
            params = action.get('limit-req-rate', action.get('block-req', {}))
            if 'reject_action' in params and params['reject_action'] == "page_template":
                if 'page_template_name' not in params:
                    error(f"page_template_name must be in limit-req-rate or block-req, filename: {filename}, line: {line(action)}")

                global_page_template_map = build_names_map(ctx, "global_page_template_map", client.get_all_global_page_templates)

                if params['page_template_name'] not in global_page_template_map:
                    error(f"page template not found, name: {params['page_template_name']}, filename: {filename}, line: {line(action)}")

        if 'global_action' in action:
            if 'global_action_name' not in action['global_action']:
                error(f"global_action_name must be in global_action, filename: {filename}, line: {line(action)}")

            global_action_map = build_names_map(ctx, "global_action_map", client.get_all_global_actions)
            if action['global_action']['global_action_name'] not in global_action_map:
                error(f"global action not found, name: {action['global_action']['global_action_name']}, filename: {filename}, line: {line(action)}")

        if 'set-error-page' in action:
            if 'file_path' in action['set-error-page']:
                global_static_file_map = build_static_file_map(ctx, "global_static_file_map")
                if action['set-error-page']['file_path'] not in global_static_file_map:
                    error(f"static file not found, name: {action['set-error-page']['file_path']}, filename: {filename}, line: {line(action)}")

            if 'page_template_name' in action['set-error-page']:
                global_page_template_map = build_names_map(ctx, "global_page_template_map", client.get_all_global_page_templates)
                if action['set-error-page']['page_template_name'] not in global_page_template_map:
                    error(f"page template not found, name: {action['set-error-page']['page_template_name']}, filename: {filename}, line: {line(action)}")

        if 'enable-basic-authentication' in action:
            if 'group_name' not in action['enable-basic-authentication']:
                error(f"group_name must be in enable-basic-authentication, filename: {filename}, line: {line(action)}")

            if 'group_type' not in action['enable-basic-authentication']:
                # default group type is app
                action['enable-basic-authentication']['group_type'] = "app"
                warn(f"the group_type not specified, default to app, filename: {filename}, line: {line(action)}")

            valid_group_type = ["app", "global"]
            if action['enable-basic-authentication']['group_type'] not in valid_group_type:
                error(f"unknown basic auth group type: {action['enable-basic-authentication']['group_type']}, filename: {filename}, line: {line(action)}")

            if action['enable-basic-authentication']['group_type'] == 'app':
                basic_auth_group_map = build_names_map(ctx, "basic_auth_group_map", client.get_all_app_basic_auth_user_groups)

                if action['enable-basic-authentication']['group_name'] not in basic_auth_group_map:
                    error(f"basic auth group not found, name: {action['enable-basic-authentication']['group_name']}, filename: {filename}, line: {line(action)}")
            else:
                global_basic_auth_group_map = build_names_map(ctx, "global_basic_auth_group_map", client.get_all_global_basic_auth_user_groups)
                if action['enable-basic-authentication']['group_name'] not in global_basic_auth_group_map:
                    error(f"global basic auth group not found, name: {action['enable-basic-authentication']['group_name']}, filename: {filename}, line: {line(action)}")

        if 'mirror-request' in action:
            if 'upstream_name' not in action['mirror-request']:
                error(f"upstream_name must be in mirror-request, filename: {filename}, line: {line(action)}")

            mirror_request_action = action['mirror-request']
            if 'upstream_type' not in mirror_request_action:
                # default group type is app
                mirror_request_action['upstream_type'] = "app"
                warn(f"upstream_type not specified, default to app, filename: {filename}, line: {line(action)}")

            valid_group_type = ["app", "global"]
            if mirror_request_action['upstream_type'] not in valid_group_type:
                error(f"unknown upstream type: {mirror_request_action['upstream_type']}, filename: {filename}, line: {line(action)}")

            if mirror_request_action['upstream_type'] == 'app':
                app_upstream_map = build_names_map(ctx, "app_upstream_map", client.get_all_upstreams, args={'detail': True})

                if mirror_request_action['upstream_name'] not in app_upstream_map:
                    error(f"upstream not found, name: {mirror_request_action['upstream_name']}, filename: {filename}, line: {line(action)}")
            else:
                global_upstream_map = build_names_map(ctx, "global_upstream_map", client.get_all_global_upstreams)
                if mirror_request_action['upstream_name'] not in global_upstream_map:
                    error(f"global upstream not found, name: {mirror_request_action['upstream_name']}, filename: {filename}, line: {line(action)}")

    return True

def check_waf(ctx, filename, rule):
    if 'waf' not in rule:
        return True

    client = ctx['client']

    waf = rule['waf']
    if not isinstance(waf, dict):
        error(f"waf must be a dict, filename: {filename}, line: {line(rule)}")

    if 'action' not in waf:
        error(f"waf must have action, filename: {filename}, line: {line(rule)}")

    if 'rule_sets' not in waf:
        error(f"waf must have rule_sets, filename: {filename}, line: {line(rule)}")

    global_waf_rule_sets_map = build_names_map(ctx, "global_waf_rule_sets_map", client.get_all_global_waf_rules)
    for rule_set in waf['rule_sets']:
        if rule_set not in global_waf_rule_sets_map:
            error(f"unknown global waf rule set: {rule_set}, filename: {filename}, line: {line(rule)}")

    return True

def check_proxy(ctx, filename, rule):
    if 'proxy' not in rule:
        return True

    exp_upstream_types = {
        'http': True,
        'http_k8s': True,
        'global': True,
        'global_k8s': True,
    }

    proxy = rule['proxy']

    if not isinstance(proxy, dict):
        error(f"proxy must be a dict, filename: {filename}, line: {line(rule)}")

    if 'upstream' in proxy:
        upstreams = proxy['upstream']
        for upstream in upstreams:
            if 'cluster_name' not in upstream:
                error(f"upstream must have cluster_name, filename: {filename}, line: {line(rule)}")
            if 'cluster_type' not in upstream:
                error(f"upstream must have cluster_type, filename: {filename}, line: {line(rule)}")
            if upstream['cluster_type'] not in exp_upstream_types:
                error(f"unknown cluster_type: {upstream['cluster_type']}, filename: {filename}, line: {line(rule)}")

    if 'backup' in proxy:
        upstreams = proxy['backup']
        for upstream in upstreams:
            if 'cluster_name' not in upstream:
                error(f"upstream must have cluster_name, filename: {filename}, line: {line(rule)}")
            if 'cluster_type' not in upstream:
                error(f"upstream must have cluster_type, filename: {filename}, line: {line(rule)}")
            if upstream['cluster_type'] not in exp_upstream_types:
                error(f"unknown cluster_type: {upstream['cluster_type']}, filename: {filename}, line: {line(rule)}")

    return True

def check_content(ctx, filename, rule):
    if 'content' not in rule:
        return True

    client = ctx['client']

    if 'file' in rule['content']:
        global_static_file_map = build_static_file_map(ctx, "global_static_file_map")
        if rule['content']['file'] not in global_static_file_map:
            error(f"global static file {rule['content']['file']} not found, filename: {filename}, line: {line(rule)}")

    return True

def check_page_rules(ctx, filename, rules):
    exp_rule = {
        'enable_rule': {
            'type': bool,
        },
        'actions': {
            'type': [dict, list],
            'require': False,
        },
        'waf': {
            'type': dict,
            'require': False,
        },
        'cache': {
            'type': dict,
            'require': False,
        },
        'content': {
            'type': dict,
            'require': False,
        },
        'conditions': {
            'type': list,
            'require': False,
        },
        'order': {
            'type': int,
        },
        'comment': {
            'type': str,
        },
    }

    for rule in rules:
        for key, expected in exp_rule.items():
            if key not in rule:
                if expected.get('require', False):
                    error(f"missing key \"{key}\" in rule, filename: {filename}, line: {line(rule)}")
                else:
                    continue

            expected_type = expected['type']
            if not check_type(rule[key], expected_type):
                error(f"incorrect type for key: {key}, expected {expected_type}, got {type(rule[key])}, filename: {filename}, line: {line(rule)}")

        check_conditions(ctx, filename, rule)
        check_actions(ctx, filename, rule)
        check_waf(ctx, filename, rule)
        check_proxy(ctx, filename, rule)
        check_content(ctx, filename, rule)

    return True

def ip_list_id_to_name(ctx, ip_list_id, ip_list_type):
    # id to name
    client = ctx['client']

    # ip_list_map = dict()
    if ip_list_type == "app-ip-list":
        client.use_app(ctx['app_id'])
        ip_list = client.get_ip_list(rule_id=ip_list_id)
        return ip_list['name']

    elif ip_list_type == "ip-list":
        ip_list = client.get_global_ip_list(rule_id=ip_list_id)
        return ip_list['name']

    else:
        error("ip_list type must be 'app-ip-list' or 'ip-list'")

def process_conditions(ctx, conditions):
    if not conditions:
        return conditions

    app_ip_list_map = ctx.get('app_ip_list_map', dict())
    global_ip_list_map = ctx.get('global_ip_list_map', dict())
    user_variable_map = ctx.get('user_variable_map', dict())
    global_variable_map = ctx.get('global_variable_map', dict())

    for condition in conditions:
        if 'user_var' in condition:
            condition['user_var'] = user_variable_map[condition['user_var']]

        if 'global_var' in condition:
            condition['global_var'] = global_variable_map[condition['global_var']]

        if 'vals' in condition:
            new_vals = list()
            for val in condition['vals']:
                if isinstance(val, dict):
                    if val['type'] == "ip-list":
                        v = global_ip_list_map[val['val']]
                    else:
                        v = app_ip_list_map[val['val']]

                    new_vals.append([ str(v), val['type'] ])
                else:
                    new_vals.append(val)

            condition['vals'] = new_vals

    return conditions

def process_upstreams(ctx, upstreams):
    client = ctx['client']

    if 'http_upstreams' not in ctx:
        ups = client.get_all_upstreams(detail=True)
        upstreams_map = dict()
        for upstream in ups:
            upstreams_map[upstream['name']] = upstream['id']
        ctx['http_upstreams'] = upstreams_map

    http_upstreams = ctx['http_upstreams']

    if 'http_k8s_upstreams' not in ctx:
        ups = client.get_all_k8s_upstreams(detail=True)
        upstreams_map = dict()
        for upstream in ups:
            upstreams_map[upstream['name']] = upstream['id']
        ctx['http_k8s_upstreams'] = upstreams_map

    http_k8s_upstreams = ctx['http_k8s_upstreams']

    if 'global_upstreams' not in ctx:
        ups = client.get_all_global_upstreams(detail=True)
        upstreams_map = dict()
        for upstream in ups:
            upstreams_map[upstream['name']] = upstream['id']
        ctx['global_upstreams'] = upstreams_map

    global_upstreams = ctx['global_upstreams']

    if 'global_k8s_upstreams' not in ctx:
        ups = client.get_all_global_k8s_upstreams(detail=True)
        upstreams_map = dict()
        for upstream in ups:
            upstreams_map[upstream['name']] = upstream['id']
        ctx['global_k8s_upstreams'] = upstreams_map

    global_k8s_upstreams = ctx['global_k8s_upstreams']

    for upstream in upstreams:
        if upstream['cluster_type'] == "http":
            upstream_id = http_upstreams.get(upstream['cluster_name'], None)
            if upstream_id is None:
                error(f"upstream not found in app, upstream name: {upstream['cluster_name']}")
            upstream['upstream'] = upstream_id
        elif upstream['cluster_type'] == "http_k8s":
            upstream_id = http_k8s_upstreams.get(upstream['cluster_name'], None)
            if upstream_id is None:
                error(f"upstream not found in app, upstream name: {upstream['cluster_name']}")
            upstream['k8s_upstream'] = upstream_id
        elif upstream['cluster_type'] == "global":
            upstream_id = global_upstreams.get(upstream['cluster_name'], None)
            if upstream_id is None:
                error(f"upstream not found in app, upstream name: {upstream['cluster_name']}")
            upstream['global_upstream'] = upstream_id
        elif upstream['cluster_type'] == "global_k8s":
            upstream_id = global_k8s_upstreams.get(upstream['cluster_name'], None)
            if upstream_id is None:
                error(f"upstream not found in app, upstream name: {upstream['cluster_name']}")
            upstream['global_k8s_upstream'] = upstream_id
        else:
            error(f"unknown cluster type: {upstream['cluster_type']}")

    return upstreams

def process_proxy(ctx, proxy):
    if proxy is None:
        return None

    # replace upstream name to id
    # replace upstreams
    if 'upstream' in proxy:
        proxy['upstream'] = process_upstreams(ctx, proxy['upstream'])

    # replace backup upstreams
    if 'backup_upstream' in proxy:
        proxy['backup_upstream'] = process_upstreams(ctx, proxy['backup_upstream'])

    return proxy

def process_content(ctx, content):
    if content is None:
        return None

    # replace upstream name to id
    # replace upstreams
    if 'file' in content:
        global_static_file_map = ctx.get('global_static_file_map', dict())
        if not content['file'] in global_static_file_map:
            error(f"file not found in global static files, file name: {content['file']}")

        content['file'] = global_static_file_map[content['file']]

    return content

def process_waf(ctx, waf):
    if waf is None:
        return None

    if 'rule_sets' in waf:
        global_waf_rule_sets_map = ctx.get('global_waf_rule_sets_map', dict())

        new_rule_sets = list()
        for rule_set in waf['rule_sets']:
            if rule_set not in global_waf_rule_sets_map:
                error(f"rule set not found in global waf rule sets, rule set name: {rule_set}")

            new_rule_sets.append(global_waf_rule_sets_map[rule_set])

        waf['rule_sets'] = new_rule_sets

    return waf

def process_user_code(ctx, action):
    # example: uuid -> partition_uuid -> [id of uuid]
    client = ctx['client']
    partition_id = ctx['partition_id']

    user_code_data = action
    if isinstance(user_code_data, dict) and 'el' in user_code_data:
        el_value = user_code_data['el']

        try:
            new_el = replace_global_variables(client, el_value, partition_id)
            new_el = page_template_name_to_id(client, new_el)
            user_code_data['el'] = new_el
        except Exception as e:
            error(f"Failed to convert global user variable name to id in Edgelang", e)

        try:
            new_el = replace_variables(client, new_el)
            user_code_data['el'] = new_el
        except Exception as e:
            error(f"Failed to convert user variable name to id in Edgelang", e)

        # TODO more replacement, such as global custom action

    return action

def process_set_var(ctx, action):
    set_var = action

    global_user_variable_map = ctx.get('global_user_variable_map', dict())
    user_variable_map = ctx.get('user_variable_map', dict())

    if set_var['var_type'] == "app":
        set_var['var_id'] = user_variable_map[set_var['var_name']]
    else:
        set_var['global_var_id'] = global_user_variable_map[set_var['var_name']]

    return action

def process_limit_action(ctx, action):
    client = ctx['client']

    global_page_template_map = ctx.get('global_page_template_map', dict())

    if ('reject_action' in action
        and action['reject_action'] == "page_template"
        and 'page_template_name' in action):

        action['page_template_id'] = global_page_template_map[action['page_template_name']]

    return action

def process_global_action(ctx, action):
    client = ctx['client']

    global_action_map = ctx.get('global_action_map', dict())

    # python sdk wants action id
    return global_action_map[action['global_action_name']]

def process_set_error_page(ctx, action):
    if 'file_path' in action:
        global_static_file_map = ctx.get('global_static_file_map', dict())
        action['file_id'] = global_static_file_map[action['file_path']]

    if 'page_template_name' in action:
        global_page_template_map = ctx.get('global_page_template_map', dict())
        action['page_template_id'] = global_page_template_map[action['page_template_name']]

    return action

def process_enable_basic_authentication(ctx, action):
    if 'group_type' in action and action['group_type'] == "global":
        global_basic_auth_group_map = ctx.get('global_basic_auth_group_map', dict())
        action['global_auth_id'] = global_basic_auth_group_map[action['group_name']]
    else:
        basic_auth_group_map = ctx.get('basic_auth_group_map', dict())
        action['app_auth_id'] = basic_auth_group_map[action['group_name']]

    return action

def process_mirror_request(ctx, action):
    if 'upstream_type' in action and action['upstream_type'] == "global":
        global_upstream_map = ctx.get('global_upstream_map', dict())
        action['global_upstream_id'] = global_upstream_map[action['upstream_name']]
    else:
        app_upstream_map = ctx.get('app_upstream_map', dict())
        action['app_upstream_id'] = app_upstream_map[action['upstream_name']]

    return action

def process_actions(ctx, actions):
    if not actions:
        return actions

    action_handlers = {
        'user-code': process_user_code,
        'set-var': process_set_var,
        'block-req': process_limit_action,
        'limit-req-rate': process_limit_action,
        'global_action': process_global_action,
        'set-error-page': process_set_error_page,
        'enable-basic-authentication': process_enable_basic_authentication,
        'mirror-request': process_mirror_request,
    }

    new_actions = list()
    for action in actions:
        for key, v in action.items():
            # skip v == {} (empty dict)
            if key in action_handlers and v:
                action[key] = action_handlers[key](ctx, v)

        new_actions.append(action)

    return new_actions

def process_page_rules(ctx):
    client = ctx['client']
    app_id = ctx['app_id']
    partition_id = ctx['partition_id']
    configs_path = ctx['configs_path']
    location = ctx.get('location', None)
    staging_release = ctx.get('staging_release', None)

    if not location:
        location = "page_rules"

    # read local rules
    configs = read_yaml_config(configs_path, location)
    if configs is None:
        return

    if not configs:
        warn("no page rules were found in the local page rules file. if you want to delete page rules from Edge Admin, please use the cleanup option.")
        return

    info("Checking if page rules have changed")

    client.use_app(app_id)

    sorted_filenames = sorted(configs.keys())

    # check local rules
    for filename in sorted_filenames:
        config = configs[filename]
        check_page_rules(ctx, filename, config)

    # calculate new rules md5
    new_rules_md5 = dict()
    for filename in sorted_filenames:
        rules = configs[filename]
        for rule in rules:
            md5 = cal_config_md5(rule)
            if md5 not in new_rules_md5:
                new_rules_md5[md5] = 0
            new_rules_md5[md5] = new_rules_md5[md5] + 1

    # read remote rules
    old_rules = client.get_all_rules(app_id)

    # remove rules no longer needed
    old_orders = list()
    keep_old_ids = dict()
    for rule in old_rules:
        old_orders.append(rule['id'])
        old_rule_md5 = get_md5_from_comment(rule.get('comment', ''))
        need_remove = False
        if old_rule_md5 not in new_rules_md5:
            need_remove = True
        else:
            new_rules_md5[old_rule_md5] = new_rules_md5[old_rule_md5] - 1
            if new_rules_md5[old_rule_md5] < 0:
                need_remove = True

        if need_remove:
            try:
                info(f"removing page rule from app, app id: {app_id}, page rule id: {rule['id']}")
                client.del_rule(rule['id'])
            except Exception as e:
                clear_changes(client, app_id)
                error(f"failed to remove page rule from app, app id: {app_id}, rule id: {rule['id']}", e)
        else:
            if old_rule_md5 not in keep_old_ids:
                keep_old_ids[old_rule_md5] = list()
            keep_old_ids[old_rule_md5].append(rule['id'])

    # add new rules and update existing ones
    order = 0
    new_orders = list()
    for filename in sorted_filenames:
        rules = configs[filename]
        for rule in rules:
            order = order + 1
            md5 = cal_config_md5(rule)

            if md5 in keep_old_ids and len(keep_old_ids[md5]) > 0:
                # rule has not changed
                first_id = keep_old_ids[md5][0]
                del keep_old_ids[md5][0]
                new_orders.append(first_id)
                continue

            # add new rule or update existing one
            conditions = process_conditions(ctx, rule.get('conditions', None))
            actions = process_actions(ctx, rule.get('actions', None))
            enable_rule = rule.get('enable_rule', True)
            cache = rule.get('cache', None)
            waf = process_waf(ctx, rule.get('waf', None))
            proxy = process_proxy(ctx, rule.get('proxy', None))
            content = process_content(ctx, rule.get('content', None))
            comment = rule.get('comment', None)
            # None means to let the SDK decide whether to set this flag
            last = rule.get('last', None)

            if comment:
                comment = get_real_comment(comment)
                comment = f"{comment}\nmd5: {md5}, please do not modify."
            else:
                comment = f"md5: {md5}, please do not modify."

            try:
                info(f"adding page rule to app, app id: {app_id}, file: {filename}, line: {line(rule)}")
                rule_id = client.new_rule(condition=conditions, conseq=actions,
                                        order=order, enable=enable_rule,
                                        comment=comment, waf=waf, proxy=proxy,
                                        cache=cache, content=content, last=last)
                new_orders.append(rule_id)
            except Exception as e:
                clear_changes(client, app_id)
                error(f"failed to add page rule to app, app id: {app_id}, file: {filename}, line: {line(rule)}", e)

    # reorder if necessary
    if old_orders != new_orders:
        order = 1
        orders = dict()
        for rule_id in new_orders:
            orders[rule_id] = order
            order = order + 1

        if orders:
            try:
                info(f"reordering the page rules, app id: {app_id}")
                client.reorder_rules(orders)
            except Exception as e:
                clear_changes(client, app_id)
                error(f"failed to reorder page rule, app id: {app_id}", e)

    release_changes(client, app_id, staging_release=staging_release)

def cleanup_page_rules(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    domain = ctx['domain']

    location = ctx.get('location', None)
    staging_release = ctx.get('staging_release', None)

    app_id = get_app_id_by_domain(client, partition_id, domain)
    if not app_id:
        if location is None:
            warn(f"app not found, domain: {domain}")
            return
        else:
            error(f"app not found, domain: {domain}")

    delete_page_rules(client, app_id)
    release_changes(client, app_id, staging_release=staging_release)

def export_conditions(ctx, cond_specs):
    if not isinstance(cond_specs, list):
        raise Exception('cond_specs must be a list')

    client = ctx['client']
    conditions = []

    for cond_spec in cond_specs:
        cond = {}

        # Process variable
        variable = cond_spec.get('variable', {})
        if 'name' in variable:
            if 'args' in variable:
                cond['var'] = [variable['name'], variable['args']]
            else:
                cond['var'] = variable['name']
        elif 'global_var' in variable:
            var = client.get_global_var(variable['global_var'])
            cond['global_var'] = var['name']
        elif 'user_var' in variable:
            var = client.get_user_var(variable['user_var'])
            cond['user_var'] = var['name']
        else:
            raise Exception('Invalid variable specification in cond_spec')

        # Process operator
        operator = cond_spec.get('operator', {})
        cond['op'] = operator.get('name', 'eq')

        # Process values
        values = cond_spec.get('values', [])
        if values:
            if len(values) == 1:
                val = values[0]
                if val['type'] == 'str':
                    cond['val'] = val['val']
                else:
                    cond['val'] = [val['val'], val['type']]
            else:
                cond['vals'] = []
                for val in values:
                    if val['type'] == 'str':
                        cond['vals'].append(val['val'])
                    else:
                        v = val['val']
                        if val['type'] == 'ip-list' or val['type'] == 'app-ip-list':
                            v = ip_list_id_to_name(ctx, v, val['type'])
                        cond['vals'].append({ 'val': v, 'type': val['type'] })
                        # cond['vals'].append(val)

        # Process caseless
        if 'caseless' in cond_spec:
            cond['caseless'] = cond_spec['caseless']

        conditions.append(cond)

    return conditions

def get_upstream_name(client, upstream_id, upstream_type):
    upstream = None
    if upstream_type == "http":
        upstream = client.get_upstream(upstream_id)
    elif upstream_type == "http_k8s":
        upstream = client.get_k8s_upstream(upstream_id)
    elif upstream_type == "global":
        upstream = client.get_global_upstream(upstream_id)
    else: # upstream_type == "global_k8s"
        upstream = client.get_global_k8s_upstream(upstream_id)

    if upstream is None:
        error(f"upstream not found, upstream id: {upstream_id}, upstream type: {upstream_type}")

    return upstream['name']

def export_upstreams(client, upstreams):
    new_upstreams = list()
    for upstream in upstreams:
        new_upstream = dict()
        upstream_id = None
        if 'cluster' in upstream:
            new_upstream['cluster_type'] = "http"
            upstream_id = upstream['cluster']
        elif 'k8s_cluster' in upstream:
            new_upstream['cluster_type'] = "http_k8s"
            upstream_id = upstream['k8s_cluster']
        elif 'global_cluster' in upstream:
            new_upstream['cluster_type'] = "global"
            upstream_id = upstream['global_cluster']
        else:
            new_upstream['cluster_type'] = "global_k8s"
            upstream_id = upstream['global_k8s_cluster']

        if 'cluster_name' in upstream:
            new_upstream['cluster_name'] = upstream['cluster_name']
        else:
            # get cluster name
            new_upstream['cluster_name'] = get_upstream_name(client, upstream_id, new_upstream['cluster_type'])

        new_upstreams.append(new_upstream)

    return new_upstreams

def export_proxy(client, proxy):
    # replace upstreams
    if 'upstream' in proxy:
        proxy['upstream'] = export_upstreams(client, proxy['upstream'])

    # replace backup upstreams
    if 'backup_upstream' in proxy:
        proxy['backup_upstream'] = export_upstreams(client, proxy['backup_upstream'])

    return proxy

def export_content(client, content):
    if not content:
        return content

    if 'file' in content:
        file = client.get_static_file(content['file'])
        content['file'] = file['path']

    return content

def export_waf(ctx, waf):
    if not waf:
        return waf

    client = ctx['client']

    if 'rule_sets' in waf:
        waf_rule_set_id_map = ctx.get('waf_rule_set_id_map', dict())
        if not waf_rule_set_id_map:
            rules = client.get_all_global_waf_rules()
            for rule in rules:
                waf_rule_set_id_map[rule['id']] = rule['name']

            ctx['waf_rule_set_id_map'] = waf_rule_set_id_map

        new_waf_rule_set = list()
        for rule_set in waf['rule_sets']:
            if rule_set not in waf_rule_set_id_map:
                error(f"WAF rule set not found: {rule_set}")

            new_waf_rule_set.append(waf_rule_set_id_map[rule_set])

        waf['rule_sets'] = new_waf_rule_set

    return waf

def export_user_code(ctx, action):
    client = ctx['client']
    partition_id = ctx['partition_id']

    user_code_data = action['user-code']
    if isinstance(user_code_data, dict) and 'el' in user_code_data:
        el_value = user_code_data['el']

        try:
            new_el = restore_global_variable_names(client, el_value, partition_id)
            new_el = page_template_id_to_name(client, new_el)
            user_code_data['el'] = new_el
        except Exception as e:
            error(f"Failed to convert global user variable id to name in Edgelang", e)

        try:
            new_el = restore_variable_names(client, new_el)
            user_code_data['el'] = new_el
        except Exception as e:
            error(f"Failed to convert user variable id to name in Edgelang", e)

        # TODO more replacement, such as global custom action
        user_code_data['el'] = format_yaml_content(user_code_data['el'])

    return action

def export_set_var(ctx, action):
    client = ctx['client']

    set_var = action['set-var']
    if 'var_id' in set_var:
        var = client.get_user_var(set_var['var_id'])
        set_var['var_name'] = var['name']
        set_var['var_type'] = "app"

    if 'global_var_id' in set_var:
        var = client.get_global_var(set_var['global_var_id'])
        set_var['var_name'] = var['name']
        set_var['var_type'] = "global"

    return action

def export_limit_action(ctx, action):
    if not action:
        return action

    if 'block-req' not in action and 'limit-req-rate' not in action:
        return action

    client = ctx['client']

    params = action.get('block-req', None)
    if params is None:
        params = action.get('limit-req-rate', None)

    if 'reject_action' in params and params['reject_action'] == "page_template":
        if 'page_template_id' not in params:
            error("not found page_template_id in action: " + str(action))

        page_template = client.get_global_page_template(params['page_template_id'])
        params['page_template_name'] = page_template['name']

        del params['page_template_id']

    return action

def export_global_action(ctx, action):
    client = ctx['client']
    global_action = client.get_global_action(action['global_action_id'])
    action['global_action_name'] = global_action['name']

    return {
        'global_action_name': global_action['name'],
    }

def export_set_error_page(ctx, action):
    client = ctx['client']

    params = action['set-error-page']
    if 'file_id' in params:
        file = client.get_static_file(params['file_id'])
        params['file_path'] = file['path']
        del params['file_id']

    if 'page_template_id' in params:
        template = client.get_global_page_template(params['page_template_id'])
        params['page_template_name'] = template['name']
        del params['page_template_id']

    return action

def export_enable_basic_authentication(ctx, action):
    client = ctx['client']

    params = action['enable-basic-authentication']
    if 'global_auth_id' in params:
        group = client.get_global_basic_auth_user_group(params['global_auth_id'])
        params['group_name'] = group['name']
        params['group_type'] = "global"
        del params['global_auth_id']

    if 'app_auth_id' in params:
        group = client.get_app_basic_auth_user_group(params['app_auth_id'])
        params['group_name'] = group['name']
        params['group_type'] = "app"
        del params['app_auth_id']

    return action

def export_mirror_request(ctx, action):
    client = ctx['client']

    params = action['mirror-request']
    if 'global_upstream_id' in params:
        record = client.get_global_upstream(params['global_upstream_id'])
        params['upstream_name'] = record['name']
        params['upstream_type'] = "global"

        del params['global_upstream_id']
        if 'cluster_name' in params:
            del params['cluster_name']

    if 'app_upstream_id' in params:
        record = client.get_upstream(params['app_upstream_id'])
        params['upstream_name'] = record['name']
        params['upstream_type'] = "app"

        del params['app_upstream_id']
        if 'cluster_name' in params:
            del params['cluster_name']

    return action

def export_actions(ctx, actions):
    client = ctx['client']
    partition_id = ctx['partition_id']

    action_handlers = {
        'user-code': export_user_code,
        'set-var': export_set_var,
        'block-req': export_limit_action,
        'limit-req-rate': export_limit_action,
        'set-error-page': export_set_error_page,
        'enable-basic-authentication': export_enable_basic_authentication,
        'mirror-request': export_mirror_request,
    }

    # if not isinstance(actions, list) and isinstance(actions, dict):
    #     new_actions = list()
    #     for k, v in actions.items():
    #         new_actions.append({k: v})
    #     actions = new_actions

    new_actions = list()
    for action in actions:
        new_action = dict()
        if 'type' in action and action['type'] in action:
            if action['type'] in action_handlers:
                action = action_handlers[action['type']](ctx, action)

            new_action[action['type']] = action[action['type']]
        else:
            if 'global_action_id' in action:
                action = export_global_action(ctx, action)
                new_action['global_action'] = action
            else:
                new_action[action['type']] = dict()

        new_actions.append(new_action)

    return new_actions

def export_page_rules(ctx):
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
    rules = client.get_all_rules(app_id)

    if not rules:
        info(f"No rules found for app_id: {app_id}")
        return

    formatted_rules = []
    order = 0
    for rule in rules:
        order = order + 1
        formatted_rule = {
            'enable_rule': rule.get('enable_rule', True),
            'order': order,
            'comment': rule.get('comment', '')
        }

        if 'conditions' in rule:
            formatted_rule['conditions'] = export_conditions(ctx, rule['conditions'])

        if 'actions' in rule:
            formatted_rule['actions'] = export_actions(ctx, rule['actions'])

        if 'waf' in rule:
            formatted_rule['waf'] = export_waf(ctx, rule['waf'])

        if 'cache' in rule:
            formatted_rule['cache'] = rule['cache']

        if 'proxy' in rule:
            formatted_rule['proxy'] = export_proxy(client, rule['proxy'])

        if 'content' in rule:
            formatted_rule['content'] = export_content(client, rule['content'])

        formatted_rules.append(formatted_rule)

    export_path = os.path.join(configs_path, 'page_rules')

    try:
        write_yaml_config(export_path, "page_rules.yaml", formatted_rules)
        info(f"Page rules exported successfully to page_rules/page_rules.yaml")
    except Exception as e:
        error(f"Failed to export page rules to page_rules/page_rules.yaml", e)
