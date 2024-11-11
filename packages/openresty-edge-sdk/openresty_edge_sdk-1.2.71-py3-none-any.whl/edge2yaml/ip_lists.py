import os
import ipaddress

from .utils import error, warn, info, get_app_id_by_domain, release_changes, \
    clear_changes, line
from .read_config import read_yaml_config, write_yaml_config

def check_ip_lists(ip_lists, filename):
    if not isinstance(ip_lists, list):
        error(f"Unsupported IP lists file format, file: {filename}")

    valid_types = ['ipv4']  # 'ipv6' not support yet
    names = dict()

    for ip_list in ip_lists:
        if not isinstance(ip_list, dict):
            error(f"Each IP list must be a dictionary, file: {filename}, line: {line(ip_list)}")

        if 'name' not in ip_list:
            error(f"Missing 'name' in IP list, file: {filename}, line: {line(ip_list)}")

        if 'type' not in ip_list:
            error(f"Missing 'type' in IP list {ip_list['name']}, file: {filename}, line: {line(ip_list)}")

        if ip_list['type'] not in valid_types:
            error(f"Invalid type '{ip_list['type']}' for IP list {ip_list['name']}, file: {filename}, line: {line(ip_list)}")

        if 'items' not in ip_list or not isinstance(ip_list['items'], list):
            error(f"Missing or invalid 'items' for IP list {ip_list['name']}, file: {filename}, line: {line(ip_list)}")

        for item in ip_list['items']:
            if not isinstance(item, dict) or 'ip' not in item:
                error(f"Invalid item format in IP list {ip_list['name']}, file: {filename}, line: {line(item)}")
            try:
                if ip_list['type'] == 'ipv4':
                    if '/' in item['ip']:
                        ipaddress.IPv4Network(item['ip'], strict=False)
                    else:
                        ipaddress.IPv4Address(item['ip'])
                else:
                    if '/' in item['ip']:
                        ipaddress.IPv6Network(item['ip'], strict=False)
                    else:
                        ipaddress.IPv6Address(item['ip'])
            except ValueError:
                error(f"Invalid IP address '{item['ip']}' in IP list {ip_list['name']}, file: {filename}, line: {line(item)}")

        if ip_list['name'] in names:
            error(f"Duplicate name in IP list {ip_list['name']}, file: {filename}, line: {line(ip_list)}")

        names[ip_list['name']] = True

    return True

def is_change_ip_list(new_list, old_list):
    if (new_list['name'] != old_list['name'] or
            new_list['type'] != old_list['type']):
        return True

    new_ips = set(item['ip'] for item in new_list['items'])
    old_ips = set(item['ip'] for item in old_list['items'])
    return new_ips != old_ips

def process_ip_lists(ctx):
    client = ctx['client']
    app_id = ctx['app_id']
    configs_path = ctx['configs_path']
    location = ctx.get('location', None)
    staging_release = ctx.get('staging_release', None)

    if not location:
        location = "ip_lists"

    configs = read_yaml_config(configs_path, location)
    if configs is None:
        return

    info("Checking if IP lists are valid")
    for filename, ip_lists in configs.items():
        check_ip_lists(ip_lists, filename)

    client.use_app(app_id)
    old_ip_lists = client.get_all_ip_lists()

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
                        info(f"Updating IP list \"{ip_list['name']}\", app id: {app_id}")
                        client.put_ip_list(
                            rule_id=old_ip_list['id'],
                            name=ip_list['name'],
                            type=ip_list['type'],
                            items=ip_list['items']
                        )
                    except Exception as e:
                        clear_changes(client, app_id)
                        error(f"Failed to update IP list, file: {filename}, line: {line(ip_list)}", e)
            else:
                try:
                    info(f"Adding IP list \"{ip_list['name']}\" to app, app id: {app_id}")
                    client.new_ip_list(
                        name=ip_list['name'],
                        type=ip_list['type'],
                        items=ip_list['items']
                    )
                except Exception as e:
                    clear_changes(client, app_id)
                    error(f"Failed to add IP list to app, file: {filename}, line: {line(ip_list)}", e)

    for list_name, ip_list in old_ip_lists_dict.items():
        if list_name not in new_ip_lists_dict:
            try:
                info(f"Removing IP list \"{list_name}\" from app, app id: {app_id}")
                client.del_ip_list(ip_list['id'])
            except Exception as e:
                clear_changes(client, app_id)
                error(f"Failed to remove IP list from app, app id: {app_id}, list id: {ip_list['id']}", e)

    release_changes(client, app_id, staging_release=staging_release)

def cleanup_ip_lists(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    domain = ctx['domain']
    staging_release = ctx.get('staging_release', None)

    app_id = get_app_id_by_domain(client, partition_id, domain)
    if not app_id:
        error(f"App not found, app id: {app_id}, domain: {domain}")

    client.use_app(app_id)
    ip_lists = client.get_all_ip_lists()

    for ip_list in ip_lists:
        try:
            info(f"Removing IP list \"{ip_list['name']}\" from app, app id: {app_id}")
            client.del_ip_list(ip_list['id'])
        except Exception as e:
            clear_changes(client, app_id)
            error(f"Failed to remove IP list from app, app id: {app_id}, list id: {ip_list['id']}", e)

    release_changes(client, app_id, staging_release=staging_release)

def export_ip_lists(ctx):
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
    ip_lists = client.get_all_ip_lists()

    if not ip_lists:
        info(f"No IP lists found for app_id: {app_id}")
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

    export_path = os.path.join(configs_path, "ip_lists")

    try:
        write_yaml_config(export_path, "ip_lists.yaml", formatted_ip_lists)
        info(f"IP lists exported successfully to ip_lists/ip_lists.yaml")
    except Exception as e:
        error(f"Failed to export IP lists to ip_lists/ip_lists.yaml", e)
