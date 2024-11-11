import os
import ipaddress

from .utils import error, warn, info, line
from .read_config import read_yaml_config, write_yaml_config
from .ip_lists import check_ip_lists, is_change_ip_list

def process_global_ip_lists(ctx):
    client = ctx['client']
    configs_path = ctx['configs_path']
    location = ctx.get('location', None)

    if not location:
        location = "global_ip_lists"

    configs = read_yaml_config(configs_path, location)
    if configs is None:
        return

    info("Checking if IP lists are valid")
    for filename, ip_lists in configs.items():
        check_ip_lists(ip_lists, filename)

    old_ip_lists = client.get_all_global_ip_lists()

    old_ip_lists_dict = {ip_list['name']: ip_list for ip_list in old_ip_lists}

    info("Checking if IP lists have changed")
    new_ip_lists_dict = {}
    sorted_configs = sorted(configs.keys())

    for filename in sorted_configs:
        ip_lists = configs[filename]
        for ip_list in ip_lists:
            new_ip_lists_dict[ip_list['name']] = True

            if ip_list['name'] in old_ip_lists_dict:
                old_ip_list = old_ip_lists_dict[ip_list['name']]
                if is_change_ip_list(ip_list, old_ip_list):
                    try:
                        info(f"Updating Global IP list \"{ip_list['name']}\"")
                        client.put_global_ip_list(
                            rule_id=old_ip_list['id'],
                            name=ip_list['name'],
                            type=ip_list['type'],
                            items=ip_list['items']
                        )
                    except Exception as e:
                        error(f"Failed to update IP list, file: {filename}, line: {line(ip_list)}", e)
            else:
                try:
                    info(f"Adding global IP list \"{ip_list['name']}\"")
                    client.new_global_ip_list(
                        name=ip_list['name'],
                        type=ip_list['type'],
                        items=ip_list['items']
                    )
                except Exception as e:
                    error(f"Failed to add IP list to app, file: {filename}, line: {line(ip_list)}", e)

    # since this is a global configuration,
    # we will not perform deletion operations in order to maintain compatibility with multiple local configurations.
    # for list_name, ip_list in old_ip_lists_dict.items():
    #     if list_name not in new_ip_lists_dict:
    #         try:
    #             info(f"Removing Global IP list \"{list_name}\"")
    #             client.del_global_ip_list(ip_list['id'])
    #         except Exception as e:
    #             error(f"Failed to remove Global IP list,list id: {ip_list['id']}", e)

def cleanup_global_ip_lists(ctx):
    pass
    # since this is a global configuration,
    # we will not perform deletion operations in order to maintain compatibility with multiple local configurations.
    # client = ctx['client']
    # partition_id = ctx['partition_id']
    # domain = ctx['domain']

    # ip_lists = client.get_all_global_ip_lists()

    # for ip_list in ip_lists:
    #     try:
    #         info(f"Removing Global IP list \"{ip_list['name']}\"")
    #         client.del_global_ip_list(ip_list['id'])
    #     except Exception as e:
    #         error(f"Failed to remove Global IP list from app, list id: {ip_list['id']}", e)

def export_global_ip_lists(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    domain = ctx['domain']
    configs_path = ctx['export_to_path']

    ip_lists = client.get_all_global_ip_lists()

    if not ip_lists:
        info(f"No IP Global lists found")
        return

    formatted_ip_lists = []
    for ip_list in ip_lists:
        items = ip_list['items']
        new_items = list()
        for item in items:
            new_items.append({'ip': item['ip']})

        formatted_list = {
            'name': ip_list['name'],
            'type': ip_list['type'],
            'items': new_items
        }
        formatted_ip_lists.append(formatted_list)

    export_path = os.path.join(configs_path, "global_ip_lists")

    try:
        write_yaml_config(export_path, "global_ip_lists.yaml", formatted_ip_lists)
        info(f"Global IP lists exported successfully to global_ip_lists/global_ip_lists.yaml")
    except Exception as e:
        error(f"Failed to export IP lists to global_ip_lists/global_ip_lists.yaml", e)
