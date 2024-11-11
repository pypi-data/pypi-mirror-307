import os

from .utils import error, warn, info, get_app_id_by_domain, is_valid_host, \
    is_valid_ipv4_address, is_valid_ipv6_address, release_changes, \
    clear_changes, line
from .read_config import read_yaml_config, write_yaml_config
from .k8s_upstreams import check_upstream_checker

def delete_app_upstreams(client, app_id):
    client.use_app(app_id)
    info(f"removing all upstream in app, app id: {app_id}")
    upstreams = client.get_all_upstreams(detail=True)
    for up in upstreams:
        if 'id' in up:
            info(f"removing upstream from app, app id: {app_id}, upstream id: {up['id']}, upstream name: {up['name']}")
            client.del_upstream(up['id'])

def check_upstreams(upstreams, filename):
    if not isinstance(upstreams, dict):
        error("unsupported upstream file format, file: {filename}")

    names = dict()
    for up_name, up in upstreams.items():
        if up_name in names:
            error(f"Duplicate name in upstream {up_name}, file: {filename}, line: {line(up)}")

        names[up_name] = True

        if not isinstance(up_name, str):
            error(f"unsupported upstream file format, file: {filename}, line: {line(up_name)}")

        if not isinstance(up, dict):
            error(f"upstream for name {up_name} must be a dict, file: {filename}, line: {line(up)}")

        ssl = up.get('ssl', False)
        if not isinstance(ssl, bool):
            error(f"ssl flag for upstream {up_name} must be a boolean, file: {filename}, line: {line(ssl)}")

        disable_ssl_verify = up.get('disable_ssl_verify', False)
        if not isinstance(disable_ssl_verify, bool):
            error(f"disable_ssl_verify flag for upstream {up_name} must be a boolean, file: {filename}, line: {line(disable_ssl_verify)}")

        check_upstream_checker(up, up_name, filename)

        servers = up.get('servers', None)
        if not isinstance(servers, list) or not all(isinstance(item, dict) for item in servers):
            error(f"upstream servers for upstream {up_name} must be a list of dictionaries, file: {filename}, line: {line(servers)}")

        for s in servers:
            host = s.get("host", None)
            port = s.get("port", None)

            if not isinstance(host, str) or not is_valid_host(host):
                error(f"invalid host in upstream {up_name}: {host}, file: {filename}, line: {line(host)}")

            if not (isinstance(port, int) and 1 <= port <= 65535):
                error(f"invalid port in upstream {up_name}: {port}, file: {filename}, line: {line(port)}")

    return True

def is_change_upstream(new_up, old_up):
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

    new_servers = new_up.get('servers', list())
    old_servers = old_up.get('nodes', list())
    if len(new_servers) != len(old_servers):
        return True

    for s1, s2 in zip(new_servers, old_servers):
        host = s1.get('host')
        if is_valid_ipv4_address(host) or is_valid_ipv6_address(host):
            # ip
            if s1.get('host') != s2.get('ip', None):
                return True
        else:
            # domain
            if s1.get('host') != s2.get('domain', None):
                return True

        if s1.get('port') != s2.get('port', None):
            return True

    # no change
    return False

def format_upstream_server(servers):
    if not isinstance(servers, list):
        return

    for s in servers:
        host = s.get('host')
        if is_valid_ipv4_address(host) or is_valid_ipv6_address(host):
            s['ip'] = host
        else:
            s['domain'] = host


def process_upstreams(ctx):
    client = ctx['client']
    app_id = ctx['app_id']
    configs_path = ctx['configs_path']
    location = ctx.get('location', None)
    staging_release = ctx.get('staging_release', None)

    if not location:
        location = "upstreams"

    configs = read_yaml_config(configs_path, location)
    if configs is None:
        # FIXME: no any upstream?
        return

    # pre check
    info("Checking if upstream is valid")
    for filename, ups in configs.items():
        # check if the upstream is valid
        check_upstreams(ups, filename)

    # get all upstreams
    client.use_app(app_id)
    # old_upstreams = client.get_all_upstreams(detail=True)
    url = f'applications/http/{app_id}/clusters?detail=1'
    old_upstreams = client.get_all(url, True)

    # array to dict
    old_upstream_dict = dict()
    for up in old_upstreams:
        old_upstream_dict[up['name']] = up

    info("Checking if upstream have changed")
    # update or add upstream to app
    new_upstream_dict = dict()
    sorted_configs = sorted(configs.keys())

    for filename in sorted_configs:
        ups = configs[filename]
        sorted_ups = sorted(ups.keys())
        for up_name in sorted_ups:
            new_up = ups[up_name]
            new_upstream_dict[up_name] = True

            checker = None
            if new_up.get('enable_checker', False):
                checker = new_up.get('checker', dict())

            if up_name in old_upstream_dict:
                # check if change
                old_up = old_upstream_dict[up_name]
                if is_change_upstream(new_up, old_up):
                    format_upstream_server(new_up['servers'])
                    try:
                        # update if changed
                        info(f"updating upstream \"{up_name}\", app id: {app_id}")
                        client.put_upstream(up_id=old_up['id'],
                                            name=up_name,
                                            servers=new_up['servers'],
                                            ssl=new_up.get('ssl', False),
                                            health_checker=checker,
                                            disable_ssl_verify=new_up.get('disable_ssl_verify', False))
                    except Exception as e:
                        clear_changes(client, app_id)
                        error(f"failed to update upstream, file: {filename}, line: {line(up_name)}", e)
                else:
                    # next upstream
                    continue
            else:
                format_upstream_server(new_up['servers'])
                try:
                    # add new upstream
                    info(f"adding upstream \"{up_name}\" to app, app id: {app_id}")
                    client.new_upstream(name=up_name,
                                        servers=new_up['servers'],
                                        ssl=new_up.get('ssl', False),
                                        health_checker=checker,
                                        disable_ssl_verify=new_up.get('disable_ssl_verify', False))
                except Exception as e:
                    clear_changes(client, app_id)
                    error(f"failed to add upstream to app, file: {filename}, line: {line(up_name)}", e)

    for up_name, up in old_upstream_dict.items():
        if up_name not in new_upstream_dict:
            try:
                info(f"removing upstream \"{up_name}\" from app, app id: {app_id}")
                client.del_upstream(up['id'])
            except Exception as e:
                clear_changes(client, app_id)
                error(f"failed to remove upstream from app, app id: {app_id}, upstream id: {up['id']}", e)

    release_changes(client, app_id, staging_release=staging_release)

def cleanup_upstreams(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    domain = ctx['domain']
    staging_release = ctx.get('staging_release', None)

    app_id = get_app_id_by_domain(client, partition_id, domain)
    if not app_id:
        error(f"App not found, app id: {app_id}, domain: {domain}")

    delete_app_upstreams(client, app_id)
    release_changes(client, app_id, staging_release=staging_release)

def export_upstreams(ctx):
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
    upstreams = client.get_all_upstreams(detail=True)
    if not upstreams:
        info(f"No upstreams found for app_id: {app_id}")
        return

    formatted_upstreams = {}
    for upstream in upstreams:
        upstream_name = upstream['name']
        formatted_upstream = {
            'ssl': upstream.get('ssl', False),
            'disable_ssl_verify': upstream.get('disable_ssl_verify', False),
            'enable_checker': upstream.get('enable_checker', False),
            'servers': []
        }

        if formatted_upstream['enable_checker']:
            formatted_upstream['checker'] = upstream.get('checker', dict())

        for node in upstream.get('nodes', []):
            server = {}
            if 'ip' in node:
                server['host'] = node['ip']
            elif 'domain' in node:
                server['host'] = node['domain']
            else:
                continue  # Skip if neither IP nor domain is present

            server['port'] = node.get('port')
            formatted_upstream['servers'].append(server)

        formatted_upstreams[upstream_name] = formatted_upstream

    export_path = os.path.join(configs_path, "upstreams")

    try:
        write_yaml_config(export_path, "upstreams.yaml", formatted_upstreams)
        info(f"Upstreams exported successfully to upstreams/upstreams.yaml")
    except Exception as e:
        error(f"Failed to export upstreams to upstreams/upstreams.yaml", e)
