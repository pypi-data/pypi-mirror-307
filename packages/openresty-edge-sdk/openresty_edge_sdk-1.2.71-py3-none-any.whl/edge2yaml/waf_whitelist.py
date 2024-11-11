import os

from .utils import error, warn, info, get_app_id_by_domain, line
from .read_config import read_yaml_config, write_yaml_config
from .page_rules import export_conditions, build_names_map

def delete_waf_whitelist(client, app_id):
    client.use_app(app_id)
    info(f"Removing all WAF whitelists in app, app id: {app_id}")
    whitelists = client.get_all_waf_whitelists()
    for whitelist in whitelists:
        if 'id' in whitelist:
            try:
                info(f"Removing WAF whitelist from app, app id: {app_id}, whitelist id: {whitelist['id']}")
                client.del_waf_whitelist(whitelist['id'])
            except Exception as e:
                error(f"Failed to add WAF whitelist to app, app id: {app_id}, file: {filename}, line: {line(whitelist)}", e)

def check_waf_whitelist(filename, whitelists, ctx):
    client = ctx['client']

    global_waf_rule_sets_map = build_names_map(ctx, "global_waf_rule_sets_map", client.get_all_global_waf_rules)

    for whitelist in whitelists:
        if 'conditions' not in whitelist or not isinstance(whitelist['conditions'], list):
            error(f"Missing or invalid 'conditions' in WAF whitelist, filename: {filename}, line: {line(whitelist)}")

        if 'rules' not in whitelist or not isinstance(whitelist['rules'], list):
            error(f"Missing or invalid 'rules' in WAF whitelist, filename: {filename}, line: {line(whitelist)}")

        for condition in whitelist['conditions']:
            if 'var' not in condition:
                error(f"Missing 'var' in condition, filename: {filename}, line: {line(condition)}")
            if 'op' not in condition:
                error(f"Missing 'op' in condition, filename: {filename}, line: {line(condition)}")
            if 'vals' not in condition and 'val' not in condition:
                error(f"Missing 'vals' or 'val' in condition, filename: {filename}, line: {line(condition)}")

        for rule in whitelist['rules']:
            if 'rule_set_id' not in rule and 'rule_set_name' not in rule:
                error(f"Missing 'rule_set_id' or 'rule_set_name' in rule, filename: {filename}, line: {line(rule)}")

            if 'rule_set_id' in rule and not isinstance(rule['rule_set_id'], int):
                error(f"'rule_set_id' should be an integer, filename: {filename}, line: {line(rule)}")

            if 'rule_set_name' in rule and rule['rule_set_name'] not in global_waf_rule_sets_map:
                error(f"Invalid 'rule_set_name' in rule, filename: {filename}, line: {line(rule)}")

            if 'rule_names' in rule and not isinstance(rule['rule_names'], list):
                error(f"Invalid 'rule_names' in rule, filename: {filename}, line: {line(rule)}")

            if 'rule_names' in rule:
                for name in rule['rule_names']:
                    if not isinstance(name, str):
                        error(f"'rule_name' should be a string, filename: {filename}, line: {line(rule)}")

    return True

def process_waf_whitelist(ctx):
    client = ctx['client']
    app_id = ctx['app_id']
    configs_path = ctx['configs_path']
    location = ctx.get('location', None)

    if not location:
        location = "waf_whitelist"

    configs = read_yaml_config(configs_path, location)
    if not configs:
        return

    info("Checking if WAF whitelists are valid")

    client.use_app(app_id)

    sorted_filenames = sorted(configs.keys())

    for filename in sorted_filenames:
        config = configs[filename]
        check_waf_whitelist(filename, config, ctx)

    # Delete all existing whitelists
    delete_waf_whitelist(client, app_id)

    global_waf_rule_sets_map = ctx.get("global_waf_rule_sets_map", {})

    # Add new whitelists
    for filename in sorted_filenames:
        whitelists = configs[filename]
        # reverse whitelists so that the most recent one is processed first
        whitelists.reverse()
        for whitelist in whitelists:
            conditions = whitelist['conditions']
            rules = whitelist['rules']

            for rule in rules:
                # convert rule_set_name to rule_set_id
                if 'rule_set_name' in rule and rule['rule_set_name'] in global_waf_rule_sets_map:
                    rule['rule_set_id'] = global_waf_rule_sets_map[rule['rule_set_name']]

            try:
                info(f"Adding WAF whitelist to app, app id: {app_id}, file: {filename}, line: {line(whitelist)}")
                client.new_waf_whitelist(condition=conditions, rules=rules)
            except Exception as e:
                error(f"Failed to add WAF whitelist to app, app id: {app_id}, file: {filename}, line: {line(whitelist)}", e)

def cleanup_waf_whitelist(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    domain = ctx['domain']

    app_id = get_app_id_by_domain(client, partition_id, domain)
    if not app_id:
        error(f"App not found, app id: {app_id}, domain: {domain}")

    delete_waf_whitelist(client, app_id)

def export_waf_whitelist(ctx):
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
    whitelists = client.get_all_waf_whitelists()
    waf_rule_sets = client.get_all_global_waf_rules()

    waf_rule_sets_map = {}
    for waf_rule_set in waf_rule_sets:
        waf_rule_sets_map[waf_rule_set['id']] = waf_rule_set['name']

    if not whitelists:
        info(f"No WAF whitelists found for app_id: {app_id}")
        return

    formatted_whitelists = []
    for whitelist in whitelists:
        formatted_whitelist = {
            'rules': []
        }

        if 'conditions' in whitelist:
            formatted_whitelist['conditions'] = export_conditions(ctx, whitelist['conditions'])

        for rule in whitelist['rules']:
            formatted_rule = {
                'rule_set_name': waf_rule_sets_map[rule['rule_set_id']]
            }

            if 'rule_names' in rule:
                formatted_rule['rule_names'] = rule['rule_names']
            formatted_whitelist['rules'].append(formatted_rule)

        if 'rule_sets' in whitelist:
            for rule_set_id in whitelist['rule_sets']:
                formatted_rule = {
                    'rule_set_name': waf_rule_sets_map[rule_set_id]
                }
                formatted_whitelist['rules'].append(formatted_rule)

        formatted_whitelists.append(formatted_whitelist)

    export_path = os.path.join(configs_path, 'waf_whitelist')

    try:
        write_yaml_config(export_path, "waf_whitelist.yaml", formatted_whitelists)
        info(f"WAF whitelists exported successfully to waf_whitelist/rules.yaml")
    except Exception as e:
        error(f"Failed to export WAF whitelists to waf_whitelist/rules.yaml", e)
