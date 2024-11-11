import os

from .utils import error, warn, info, is_valid_host, \
    is_valid_ipv4_address, is_valid_ipv6_address, line
from .read_config import read_yaml_config, write_yaml_config
from .k8s_upstreams import check_upstream_checker

def process_global_upstreams(ctx):
    client = ctx['client']
    configs_path = ctx['configs_path']
    location = ctx.get('location', None)

    if not location:
        location = "global_upstreams"

    configs = read_yaml_config(configs_path, location)
    if configs is None:
        return

    info("Checking if global upstreams are valid")
    for filename, upstreams in configs.items():
        check_global_upstreams(upstreams, filename)

    old_upstreams = client.get_all_global_upstreams(detail=True)

    old_upstreams_dict = {upstream['name']: upstream for upstream in old_upstreams}

    info("Checking if global upstreams have changed")
    new_upstreams_dict = {}
    sorted_configs = sorted(configs.keys())

    for filename in sorted_configs:
        upstreams = configs[filename]
        for up_name, up in upstreams.items():
            new_upstreams_dict[up_name] = True

            checker = None
            if up.get('enable_checker', False):
                checker = up.get('checker', dict())

            if up_name in old_upstreams_dict:
                old_up = old_upstreams_dict[up_name]
                if is_change_global_upstream(up, old_up):
                    try:
                        info(f"Updating Global upstream \"{up_name}\"")
                        client.put_global_upstream(
                            up_id=old_up['id'],
                            name=up_name,
                            ssl=up.get('ssl', False),
                            health_checker=checker,
                            disable_ssl_verify=up.get('disable_ssl_verify', False),
                            servers=format_upstream_server(up['servers'])
                        )
                    except Exception as e:
                        error(f"Failed to update global upstream, file: {filename}, line: {line(up)}", e)
            else:
                try:
                    info(f"Adding global upstream \"{up_name}\"")
                    client.new_global_upstream(
                        name=up_name,
                        ssl=up.get('ssl', False),
                        disable_ssl_verify=up.get('disable_ssl_verify', False),
                        health_checker=checker,
                        servers=format_upstream_server(up['servers'])
                    )
                except Exception as e:
                    error(f"Failed to add global upstream, file: {filename}, line: {line(up)}", e)

    # since this is a global configuration,
    # we will not perform deletion operations in order to maintain compatibility with multiple local configurations.
    # for up_name, up in old_upstreams_dict.items():
    #     if up_name not in new_upstreams_dict:
    #         try:
    #             info(f"Removing Global upstream \"{up_name}\"")
    #             client.del_global_upstream(up['id'])
    #         except Exception as e:
    #             error(f"Failed to remove Global upstream, upstream id: {up['id']}", e)

def cleanup_global_upstreams(ctx):
    pass
    # since this is a global configuration,
    # we will not perform deletion operations in order to maintain compatibility with multiple local configurations.
    # client = ctx['client']

    # upstreams = client.get_all_global_upstreams()

    # for upstream in upstreams:
    #     try:
    #         info(f"Removing Global upstream \"{upstream['name']}\"")
    #         client.del_global_upstream(upstream['id'])
    #     except Exception as e:
    #         error(f"Failed to remove Global upstream, upstream id: {upstream['id']}", e)

def export_global_upstreams(ctx):
    client = ctx['client']
    configs_path = ctx['export_to_path']

    upstreams = client.get_all_global_upstreams(detail=True)

    if not upstreams:
        info(f"No Global upstreams found")
        return

    formatted_upstreams = {}
    for upstream in upstreams:
        formatted_upstream = {
            'ssl': upstream.get('ssl', False),
            'disable_ssl_verify': upstream.get('disable_ssl_verify', False),
            'enable_checker': upstream.get('enable_checker', False),
            'servers': []
        }

        if formatted_upstream['enable_checker']:
            formatted_upstream['checker'] = upstream.get('checker', {})

        for node in upstream.get('nodes', []):
            server = {}
            if 'ip' in node:
                server['host'] = node['ip']
            elif 'domain' in node:
                server['host'] = node['domain']
            else:
                continue

            server['port'] = node.get('port')
            formatted_upstream['servers'].append(server)

        formatted_upstreams[upstream['name']] = formatted_upstream

    export_path = os.path.join(configs_path, "global_upstreams")

    try:
        write_yaml_config(export_path, "global_upstreams.yaml", formatted_upstreams)
        info(f"Global upstreams exported successfully to global_upstreams/global_upstreams.yaml")
    except Exception as e:
        error(f"Failed to export global upstreams to global_upstreams/global_upstreams.yaml", e)

def check_global_upstreams(upstreams, filename):
    if not isinstance(upstreams, dict):
        error(f"Unsupported global upstream file format, file: {filename}")

    for up_name, up in upstreams.items():
        if not isinstance(up_name, str):
            error(f"Unsupported global upstream name format, file: {filename}, line: {line(up_name)}")

        if not isinstance(up, dict):
            error(f"Global upstream for name {up_name} must be a dict, file: {filename}, line: {line(up)}")

        ssl = up.get('ssl', False)
        if not isinstance(ssl, bool):
            error(f"ssl flag for global upstream {up_name} must be a boolean, file: {filename}, line: {line(ssl)}")

        disable_ssl_verify = up.get('disable_ssl_verify', False)
        if not isinstance(disable_ssl_verify, bool):
            error(f"disable_ssl_verify flag for global upstream {up_name} must be a boolean, file: {filename}, line: {line(disable_ssl_verify)}")

        enable_checker = up.get('enable_checker', False)
        if not isinstance(enable_checker, bool):
            error(f"enable_checker flag for global upstream {up_name} must be a boolean, file: {filename}, line: {line(enable_checker)}")

        if enable_checker:
            check_upstream_checker(up, up_name, filename)

        servers = up.get('servers', None)
        if not isinstance(servers, list) or not all(isinstance(item, dict) for item in servers):
            error(f"Global upstream servers for upstream {up_name} must be a list of dictionaries, file: {filename}, line: {line(servers)}")

        for s in servers:
            host = s.get("host", None)
            port = s.get("port", None)

            if not isinstance(host, str) or not is_valid_host(host):
                error(f"Invalid host in global upstream {up_name}: {host}, file: {filename}, line: {line(host)}")

            if not (isinstance(port, int) and 1 <= port <= 65535):
                error(f"Invalid port in global upstream {up_name}: {port}, file: {filename}, line: {line(port)}")

def is_change_global_upstream(new_up, old_up):
    if new_up.get('ssl', False) != old_up.get('ssl', False):
        return True

    if new_up.get('disable_ssl_verify', False) != old_up.get('disable_ssl_verify', False):
        return True

    if new_up.get('enable_checker', False) != old_up.get('enable_checker', False):
        return True

    if new_up.get('enable_checker', False) is True:
        new_checker = new_up.get('checker', dict())
        old_checker = old_up.get('checker', dict())
        for key in new_checker:
            if new_checker[key] != old_checker[key]:
                return True

    new_servers = new_up.get('servers', [])
    old_servers = old_up.get('nodes', [])
    if len(new_servers) != len(old_servers):
        return True

    for s1, s2 in zip(new_servers, old_servers):
        host = s1.get('host')
        if is_valid_ipv4_address(host) or is_valid_ipv6_address(host):
            if s1.get('host') != s2.get('ip', None):
                return True
        else:
            if s1.get('host') != s2.get('domain', None):
                return True

        if s1.get('port') != s2.get('port', None):
            return True

    return False

def format_upstream_server(servers):
    formatted_servers = []
    for s in servers:
        server = {}
        host = s.get('host')
        if is_valid_ipv4_address(host) or is_valid_ipv6_address(host):
            server['ip'] = host
        else:
            server['domain'] = host
        server['port'] = s.get('port')
        formatted_servers.append(server)
    return formatted_servers
