import os
import re

from .utils import error, warn, info, line
from .read_config import read_yaml_config, write_yaml_config, format_yaml_content

def process_global_page_templates(ctx):
    client = ctx['client']
    configs_path = ctx['configs_path']
    location = ctx.get('location', None)

    if not location:
        location = "global_page_templates"

    configs = read_yaml_config(configs_path, location)
    if configs is None:
        return

    info("Checking if page templates are valid")
    for filename, page_templates in configs.items():
        check_page_templates(page_templates, filename)

    old_page_templates = client.get_all_global_page_templates()

    old_page_templates_dict = {template['name']: template for template in old_page_templates}

    info("Checking if page templates have changed")
    new_page_templates_dict = {}
    sorted_configs = sorted(configs.keys())

    for filename in sorted_configs:
        page_templates = configs[filename]
        for template in page_templates:
            new_page_templates_dict[template['name']] = True

            if template['name'] in old_page_templates_dict:
                old_template = old_page_templates_dict[template['name']]
                if is_change_page_template(template, old_template):
                    try:
                        info(f"Updating Global page template \"{template['name']}\"")
                        client.put_global_page_template(
                            id=old_template['id'],
                            name=template['name'],
                            content=template['content']
                        )
                    except Exception as e:
                        error(f"Failed to update page template, file: {filename}, line: {line(template)}", e)
            else:
                try:
                    info(f"Adding global page template \"{template['name']}\"")
                    client.new_global_page_template(
                        name=template['name'],
                        content=template['content']
                    )
                except Exception as e:
                    error(f"Failed to add page template, file: {filename}, line: {line(template)}", e)

    # since this is a global configuration,
    # we will not perform deletion operations in order to maintain compatibility with multiple local configurations.
    # for template_name, template in old_page_templates_dict.items():
    #     if template_name not in new_page_templates_dict:
    #         try:
    #             info(f"Removing Global page template \"{template_name}\"")
    #             client.del_global_page_template(template['id'])
    #         except Exception as e:
    #             error(f"Failed to remove Global page template, template id: {template['id']}", e)

def cleanup_global_page_templates(ctx):
    pass
    # since this is a global configuration,
    # we will not perform deletion operations in order to maintain compatibility with multiple local configurations.
    # client = ctx['client']
    # partition_id = ctx['partition_id']

    # page_templates = client.get_all_global_page_templates()

    # for template in page_templates:
    #     try:
    #         info(f"Removing Global page template \"{template['name']}\"")
    #         client.del_global_page_template(template['id'])
    #     except Exception as e:
    #         error(f"Failed to remove Global page template, template id: {template['id']}", e)

def export_global_page_templates(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    configs_path = ctx['export_to_path']

    page_templates = client.get_all_global_page_templates()

    if not page_templates:
        info(f"No Global page templates found")
        return


    formatted_page_templates = []
    for template in page_templates:
        formatted_template = {
            'name': template['name'],
            'content': format_yaml_content(template['content'])
        }
        formatted_page_templates.append(formatted_template)

    export_path = os.path.join(configs_path, "global_page_templates")

    try:
        write_yaml_config(export_path, "global_page_templates.yaml", formatted_page_templates)
        info(f"Page templates exported successfully to global_page_templates/global_page_templates.yaml")
    except Exception as e:
        error(f"Failed to export page templates to global_page_templates/global_page_templates.yaml", e)

def check_page_templates(page_templates, filename):
    for template in page_templates:
        if 'name' not in template:
            error(f"Page template missing 'name' field in file: {filename}, line: {line(template)}")
        if 'content' not in template:
            error(f"Page template missing 'content' field in file: {filename}, line: {line(template)}")

def is_change_page_template(new_template, old_template):
    return new_template['content'] != old_template['content']

def name_to_id(client, content):
    if not isinstance(content, str):
        raise Exception("bad content")

    matched_items = []
    pattern = r'\$or_global_page_template_[a-zA-Z0-9_-]+'
    matched_items = re.findall(pattern, content)
    unique_matched_items = list(set(matched_items))

    names = {}
    for var in unique_matched_items:
        match = re.search(r'\$or_global_page_template_(.*)', var)
        # should always match
        name = match.group(1)
        names[var] = name

    templates = client.get_all_global_page_templates()
    if not isinstance(templates, list):
        templates = list()

    template_names = {}
    for t in templates:
        template_names[t['name']] = t['id']

    data = client.get_sync_to_all()
    ngx_sync_to_all = True
    if data and data.get('ngx', True) == False:
        ngx_sync_to_all = False

    for fake_name, name in names.items():
        if name in template_names:
            var_id = template_names[name]
        else:
            raise Exception(f"global page templates not found in Edge Admin: {name}")

        content = content.replace(fake_name, f'{var_id}')

    return content

def replace_global_page_template_in_el(client, actions, filename):
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
            user_code_data['el'] = name_to_id(client, el_value)
        except Exception as e:
            error(f"failed to replace global variable in Edgelang, file: {filename}, line: {line(user_code_data)}", e)

def id_to_name(client, content):
    if not isinstance(content, str):
        raise Exception("Bad content")

    pattern = r'page-template-id:\s*\d+'
    matched_items = re.findall(pattern, content)

    templates = client.get_all_global_page_templates()
    if not isinstance(templates, list):
        templates = []

    template_ids = {var['id']: var['name'] for var in templates}

    for var in matched_items:
        match = re.search(r'page-template-id:\s*(\d+)', var)
        if match:
            var_id = int(match.group(1))
            if var_id in template_ids:
                var_name = template_ids[var_id]
                content = content.replace(var, f'page-template-id: $or_global_page_template_{var_name}')
            else:
                warn(f"Global page template ID not found: {var_id}")

    return content

def restore_global_page_template_names_in_el(client, actions):
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
                user_code_data['el'] = id_to_name(client, el_value)
            except Exception as e:
                error(f"Failed to restore global page template names in Edgelang", e)
