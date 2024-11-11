import os

from .utils import error, warn, info, get_app_id_by_domain, line, is_partition_action
from .read_config import read_yaml_config, write_yaml_config, format_yaml_content
from .global_variables import replace_global_variable_in_el, restore_global_variable_names_in_el
from .global_page_templates import replace_global_page_template_in_el, restore_global_page_template_names_in_el
from .page_rules import export_conditions

def check_global_custom_actions(filename, actions):
    for action in actions:
        if 'name' not in action:
            error(f"Missing 'name' in global custom action, filename: {filename}, line: {line(action)}")

        if 'conditions' in action and not isinstance(action['conditions'], list):
            error(f"Invalid 'conditions' in global custom action {action['name']}, filename: {filename}, line: {line(action)}")

        if 'actions' not in action or not (isinstance(action['actions'], dict) or isinstance(action['actions'], list)):
            error(f"Missing or invalid 'actions' in global custom action {action['name']}, filename: {filename}, line: {line(action)}")

        if 'conditions' in action:
            for condition in action['conditions']:
                if 'var' not in condition:
                    error(f"Missing 'var' in condition, action: {action['name']}, filename: {filename}, line: {line(condition)}")
                if 'op' not in condition:
                    error(f"Missing 'op' in condition, action: {action['name']}, filename: {filename}, line: {line(condition)}")
                if 'vals' not in condition and 'val' not in condition:
                    error(f"Missing 'vals' or 'val' in condition, action: {action['name']}, filename: {filename}, line: {line(condition)}")

    return True

def get_all_global_actions(client, detail=False):
    return client.get_all_global_actions(detail=detail)

def is_changed(ctx, new_rule, old_rule):
    old_rule_actions = list()
    rule_actions = old_rule['actions']
    for rule_action in rule_actions:
        new_action = dict()
        if 'type' in rule_action and rule_action['type'] in rule_action:
            new_action[rule_action['type']] = rule_action[rule_action['type']]
        else:
            new_action[rule_action['type']] = dict()

        old_rule_actions.append(new_action)

    old_conditions = list()
    if "conditions" in old_rule:
        old_conditions = export_conditions(ctx, old_rule['conditions'])

    if new_rule['name'] != old_rule['name']:
        return True
    if new_rule.get("conditions", list()) != old_conditions:
        return True
    if new_rule['actions'] != old_rule_actions:
        return True

    return False

def process_global_custom_actions(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    configs_path = ctx['configs_path']
    location = ctx.get('location', None)

    if not location:
        location = "global_custom_actions"

    configs = read_yaml_config(configs_path, location)
    if not configs:
        return

    info("Checking if global custom actions are valid")

    sorted_filenames = sorted(configs.keys())

    for filename in sorted_filenames:
        config = configs[filename]
        check_global_custom_actions(filename, config)

    # Get existing global custom actions
    existing_actions = get_all_global_actions(client, True)
    existing_actions_dict = {action['name']: action for action in existing_actions}

    # Process actions
    for filename in sorted_filenames:
        actions = configs[filename]
        for action in actions:
            name = action['name']
            conditions = action.get('conditions', None)
            actions_config = action['actions']

            replace_global_variable_in_el(client, actions_config, filename, partition_id)
            replace_global_page_template_in_el(client, actions_config, filename)

            if name in existing_actions_dict:
                if is_changed(ctx, action, existing_actions_dict[name]):
                    # Update existing action
                    try:
                        info(f"Updating global custom action \"{name}\", partition id: {partition_id}")
                        client.put_global_action(
                            name=name,
                            action_id=existing_actions_dict[name]['id'],
                            condition=conditions,
                            conseq=actions_config
                        )
                    except Exception as e:
                        error(f"Failed to update global custom action, file: {filename}, line: {line(action)}", e)
            else:
                # Add new action
                try:
                    info(f"Adding global custom action \"{name}\" to partition, partition id: {partition_id}")
                    client.new_global_action(
                        name=name,
                        condition=conditions,
                        conseq=actions_config
                    )
                except Exception as e:
                    error(f"Failed to add global custom action to partition, file: {filename}, line: {line(action)}", e)

            # Remove processed action from existing_actions_dict
            existing_actions_dict.pop(name, None)

    # since this is a global configuration,
    # we will not perform deletion operations in order to maintain compatibility with multiple local configurations.
    # Remove actions that are no longer in the config
    # for name, action in existing_actions_dict.items():
    #     try:
    #         info(f"Removing global custom action \"{name}\" from partition, partition id: {partition_id}")
    #         client.del_global_action(action['id'])
    #     except Exception as e:
    #         error(f"Failed to remove global custom action from partition, partition id: {partition_id}, action id: {action['id']}", e)

def cleanup_global_custom_actions(ctx):
    pass
    # since this is a global configuration,
    # we will not perform deletion operations in order to maintain compatibility with multiple local configurations.
    # client = ctx['client']
    # partition_id = ctx['partition_id']

    # actions = get_all_global_actions(client)

    # for action in actions:
    #     try:
    #         info(f"Removing global custom action \"{action['name']}\" from partition, partition id: {partition_id}")
    #         client.del_global_action(action['id'])
    #     except Exception as e:
    #         error(f"Failed to remove global custom action from partition, partition id: {partition_id}, action id: {action['id']}", e)

def export_global_custom_actions(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    configs_path = ctx['export_to_path']

    actions = get_all_global_actions(client, True)

    if not actions:
        info(f"No global custom actions found for partition_id: {partition_id}")
        return

    formatted_actions = []
    for action in actions:
        new_actions = list()
        rule_actions = action['actions']
        restore_global_variable_names_in_el(client, rule_actions, partition_id)
        restore_global_page_template_names_in_el(client, rule_actions)
        for rule_action in rule_actions:
            new_action = dict()
            if 'type' in rule_action and rule_action['type'] in rule_action:
                new_action[rule_action['type']] = rule_action[rule_action['type']]

                if rule_action['type'] == 'user-code':
                    ac = rule_action[rule_action['type']]
                    if 'el' in ac:
                        ac['el'] = format_yaml_content(ac['el'])
            else:
                new_action[rule_action['type']] = dict()

            new_actions.append(new_action)

        formatted_action = {
            'name': action['name'],
            'actions': new_actions
        }

        if 'conditions' in action:
            formatted_action['conditions'] = export_conditions(ctx, action['conditions'])

        formatted_actions.append(formatted_action)

    export_path = os.path.join(configs_path, 'global_custom_actions')

    try:
        write_yaml_config(export_path, "global_custom_actions.yaml", formatted_actions)
        info(f"Global custom actions exported successfully to global_custom_actions/global_custom_actions.yaml")
    except Exception as e:
        error(f"Failed to export global custom actions to global_custom_actions/global_custom_actions.yaml", e)
