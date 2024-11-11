import os

from .utils import error, warn, info, get_app_id_by_domain, release_changes, \
    clear_changes, line
from .read_config import read_yaml_config, write_yaml_config, format_yaml_content
from .global_variables import restore_global_variable_names, replace_global_variables
from .user_variables import restore_variable_names, replace_variables
from .global_page_templates import id_to_name as page_template_id_to_name, name_to_id as page_template_name_to_id

def check_edgelang_rules(rules, filename):
    if not isinstance(rules, list):
        error(f"Unsupported EdgeLang rules file format, file: {filename}")

    valid_types = ['before', 'after']

    for rule in rules:
        if not isinstance(rule, dict):
            error(f"Each EdgeLang rule must be a dictionary, file: {filename}, line: {line(rule)}")

        if 'type' not in rule:
            error(f"Missing 'type' in EdgeLang rule, file: {filename}, line: {line(rule)}")

        if rule['type'] not in valid_types:
            error(f"Invalid type '{rule['type']}' for EdgeLang rule, file: {filename}, line: {line(rule)}")

        if 'code' not in rule or not isinstance(rule['code'], str):
            error(f"Missing or invalid 'code' for EdgeLang rule, file: {filename}, line: {line(rule)}")

    return True

def is_change_edgelang_rule(new_code, old_code):
    return new_code != old_code

def process_edgelang_rules(ctx):
    client = ctx['client']
    app_id = ctx['app_id']
    partition_id = ctx['partition_id']
    configs_path = ctx['configs_path']
    location = ctx.get('location', None)
    staging_release = ctx.get('staging_release', None)

    if not location:
        location = "edgelang_rules"

    configs = read_yaml_config(configs_path, location)
    if configs is None:
        return

    info("Checking if EdgeLang rules are valid")
    for filename, rules in configs.items():
        check_edgelang_rules(rules, filename)

    client.use_app(app_id)
    old_rules_dict = client.get_el()

    info("Checking if EdgeLang rules have changed")
    new_rules_dict = {}
    sorted_configs = sorted(configs.keys())

    for filename in sorted_configs:
        rules = configs[filename]
        for rule in rules:
            pre = False
            if rule['type'] == "before":
                pre = True

            post = False
            if rule['type'] == "after":
                post = True

            new_rules_dict[rule['type']] = True

            try:
                rule['code'] = replace_global_variables(client, rule['code'], partition_id)
                rule['code'] = page_template_name_to_id(client, rule['code'])
            except Exception as e:
                error(f"Failed to convert global user variable name to id in Edgelang", e)

            try:
                rule['code'] = replace_variables(client, rule['code'])
            except Exception as e:
                error(f"Failed to convert user variable name to id in Edgelang", e)

            if rule['type'] in old_rules_dict:
                old_code = old_rules_dict[rule['type']]
                if is_change_edgelang_rule(rule['code'], old_code):
                    try:
                        info(f"Updating EdgeLang rule \"{rule['type']}\", app id: {app_id}")
                        client.new_el(
                            phase='req-rewrite',
                            code=rule['code'],
                            pre=pre,
                            post=post
                        )
                    except Exception as e:
                        clear_changes(client, app_id)
                        error(f"Failed to update EdgeLang rule, file: {filename}, line: {line(rule)}", e)
            else:
                try:
                    info(f"Adding EdgeLang rule \"{rule['type']}\" to app, app id: {app_id}")
                    client.new_el(
                        phase='req-rewrite',
                        code=rule['code'],
                        pre=pre,
                        post=post
                    )
                except Exception as e:
                    clear_changes(client, app_id)
                    error(f"Failed to add EdgeLang rule to app, file: {filename}, line: {line(rule)}", e)

    for rule_type, rule in old_rules_dict.items():
        pre = False
        if rule_type == "before":
            pre = True

        post = False
        if rule_type == "after":
            post = True

        if rule_type not in new_rules_dict:
            try:
                info(f"Removing EdgeLang rule \"{rule_type}\" from app, app id: {app_id}")
                client.new_el("req-rewrite", code="", pre=pre, post=post)
            except Exception as e:
                clear_changes(client, app_id)
                error(f"Failed to remove EdgeLang rule from app, app id: {app_id}, rule id: {rule['id']}", e)

    release_changes(client, app_id, staging_release=staging_release)

def cleanup_edgelang_rules(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    domain = ctx['domain']
    staging_release = ctx.get('staging_release', None)

    app_id = get_app_id_by_domain(client, partition_id, domain)
    if not app_id:
        error(f"App not found, app id: {app_id}, domain: {domain}")

    client.use_app(app_id)
    old_rules_dict = client.get_el()

    for rule_type, rule in old_rules_dict.items():
        pre = False
        if rule_type == "before":
            pre = True

        post = False
        if rule_type == "after":
            post = True

        try:
            info(f"Removing EdgeLang rule \"{rule_type}\" from app, app id: {app_id}")
            client.new_el("req-rewrite", code="", pre=pre, post=post)
        except Exception as e:
            clear_changes(client, app_id)
            error(f"Failed to remove EdgeLang rule from app, app id: {app_id}, rule id: {rule['id']}", e)

    release_changes(client, app_id, staging_release=staging_release)

def export_edgelang_rules(ctx):
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
    rules_dict = client.get_el()

    if not rules_dict:
        info(f"No EdgeLang rules found for app_id: {app_id}")
        return

    formatted_rules = []
    for rule_type, rule_code in rules_dict.items():
        try:
            rule_code = restore_global_variable_names(client, rule_code, partition_id)
            rule_code = page_template_id_to_name(client, rule_code)
        except Exception as e:
            error(f"Failed to export global user variable names in Edgelang", e)

        try:
            rule_code = restore_variable_names(client, rule_code)
        except Exception as e:
            error(f"Failed to export user variable names in Edgelang", e)

        formatted_rule = {
            'type': rule_type,
            'code': format_yaml_content(rule_code)
        }
        formatted_rules.append(formatted_rule)

    export_path = os.path.join(configs_path, "edgelang_rules")

    try:
        write_yaml_config(export_path, "edgelang_rules.yaml", formatted_rules)
        info(f"EdgeLang rules exported successfully to edgelang_rules/edgelang_rules.yaml")
    except Exception as e:
        error(f"Failed to export EdgeLang rules to edgelang_rules/edgelang_rules.yaml", e)
