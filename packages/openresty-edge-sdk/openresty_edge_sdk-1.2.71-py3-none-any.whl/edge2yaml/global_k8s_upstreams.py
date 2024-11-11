import os

from .utils import error, warn, info, line
from .read_config import read_yaml_config, write_yaml_config
from .k8s_upstreams import check_upstream_checker

def process_global_k8s_upstreams(ctx):
    client = ctx['client']
    configs_path = ctx['configs_path']
    location = ctx.get('location', None)

    if not location:
        location = "global_k8s_upstreams"

    configs = read_yaml_config(configs_path, location)
    if configs is None:
        return

    k8s_clusters = client.get_all_global_k8s()
    k8s_cluster_names = {cluster['name']: cluster['id'] for cluster in k8s_clusters}

    info("Checking if global k8s upstream is valid")
    for filename, ups in configs.items():
        check_global_k8s_upstreams(ups, filename, k8s_cluster_names)

    ups = convert_k8s_cluster_names(ups, k8s_cluster_names)

    old_upstreams = client.get_all_global_k8s_upstreams(detail=True)

    old_upstream_dict = {up['name']: up for up in old_upstreams}

    info("Checking if global k8s upstream have changed")
    new_upstream_dict = {}
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
                old_up = old_upstream_dict[up_name]
                if is_change_global_k8s_upstream(new_up, old_up):
                    try:
                        info(f"Updating global k8s upstream \"{up_name}\"")
                        client.put_global_k8s_upstream(
                            up_id=old_up['id'],
                            name=up_name,
                            k8s_services=new_up['k8s_services'],
                            ssl=new_up.get('ssl', False),
                            disable_ssl_verify=new_up.get('disable_ssl_verify', False),
                            health_checker=checker,
                        )
                    except Exception as e:
                        error(f"Failed to update global k8s upstream, file: {filename}, line: {line(new_up)}", e)
            else:
                try:
                    info(f"Adding global k8s upstream \"{up_name}\"")
                    client.new_global_k8s_upstream(
                        name=up_name,
                        k8s_services=new_up['k8s_services'],
                        ssl=new_up.get('ssl', False),
                        disable_ssl_verify=new_up.get('disable_ssl_verify', False),
                        health_checker=checker
                    )
                except Exception as e:
                    error(f"Failed to add global k8s upstream, file: {filename}, line: {line(new_up)}", e)

    # since this is a global configuration,
    # we will not perform deletion operations in order to maintain compatibility with multiple local configurations.
    # for up_name, up in old_upstream_dict.items():
    #     if up_name not in new_upstream_dict:
    #         try:
    #             info(f"Removing global k8s upstream \"{up_name}\"")
    #             client.del_global_k8s_upstream(up['id'])
    #         except Exception as e:
    #             error(f"Failed to remove global k8s upstream, upstream id: {up['id']}", e)

def cleanup_global_k8s_upstreams(ctx):
    pass
    # since this is a global configuration,
    # we will not perform deletion operations in order to maintain compatibility with multiple local configurations.
    # client = ctx['client']

    # global_k8s_upstreams = client.get_all_global_k8s_upstreams(detail=False)

    # for up in global_k8s_upstreams:
    #     up_name = up['name']
    #     up_id = up['id']

    #     try:
    #         info(f"Removing global k8s upstream \"{up_name}\"(id: {up_id})")
    #         client.del_global_k8s_upstream(up_id)
    #     except Exception as e:
    #         error(f"Failed to remove global k8s upstream: {up_name}(id: {up_id})", e)

def export_global_k8s_upstreams(ctx):
    client = ctx['client']
    configs_path = ctx['export_to_path']

    global_k8s_upstreams = client.get_all_global_k8s_upstreams(detail=True)

    if not global_k8s_upstreams:
        info(f"No global k8s upstreams found")
        return

    k8s_clusters = client.get_all_global_k8s()
    k8s_cluster_ids = {cluster['id']: cluster['name'] for cluster in k8s_clusters}

    formatted_upstreams = {}
    for upstream in global_k8s_upstreams:
        upstream_name = upstream['name']
        k8s_services = upstream.get('k8s_services', [])
        new_k8s_services = []
        for service in k8s_services:
            k8s_name = k8s_cluster_ids.get(service['k8s'])
            if k8s_name is None:
                error(f"k8s cluster not found, k8s id: {service['k8s']}")

            new_service = {
                "k8s_name": k8s_name,
                "k8s_namespace": service['k8s_namespace'],
                "k8s_service": service['k8s_service'],
                "k8s_service_port": service['k8s_service_port'],
            }

            new_k8s_services.append(new_service)

        formatted_upstream = {
            'ssl': upstream.get('ssl', False),
            'disable_ssl_verify': upstream.get('disable_ssl_verify', False),
            'enable_checker': upstream.get('enable_checker', False),
            'k8s_services': new_k8s_services
        }

        if formatted_upstream['enable_checker']:
            formatted_upstream['checker'] = upstream.get('checker', {})

        formatted_upstreams[upstream_name] = formatted_upstream

    export_path = os.path.join(configs_path, "global_k8s_upstreams")

    try:
        write_yaml_config(export_path, "global_k8s_upstreams.yaml", formatted_upstreams)
        info(f"Global k8s upstreams exported successfully to global_k8s_upstreams/global_k8s_upstreams.yaml")
    except Exception as e:
        error(f"Failed to export global k8s upstreams to global_k8s_upstreams/global_k8s_upstreams.yaml", e)

def check_global_k8s_upstreams(upstreams, filename, k8s_cluster_names):
    if not isinstance(upstreams, dict):
        error(f"Unsupported global k8s upstream file format, file: {filename}")

    for up_name, up in upstreams.items():
        if not isinstance(up, dict):
            error(f"Global k8s upstream for name {up_name} must be a dict, file: {filename}, line: {line(up)}")

        ssl = up.get('ssl', False)
        if not isinstance(ssl, bool):
            error(f"ssl flag for global k8s upstream {up_name} must be a boolean, file: {filename}, line: {line(ssl)}")

        disable_ssl_verify = up.get('disable_ssl_verify', False)
        if not isinstance(disable_ssl_verify, bool):
            error(f"disable_ssl_verify flag for global k8s upstream {up_name} must be a boolean, file: {filename}, line: {line(disable_ssl_verify)}")

        check_upstream_checker(up, up_name, filename)

        k8s_services = up.get('k8s_services', None)
        if not isinstance(k8s_services, list) or not all(isinstance(item, dict) for item in k8s_services):
            error(f"k8s_services for global k8s upstream {up_name} must be a list of dictionaries, file: {filename}, line: {line(k8s_services)}")

        for s in k8s_services:
            required_keys = ['k8s_name', 'k8s_namespace', 'k8s_service', 'k8s_service_port']
            for key in required_keys:
                if key not in s:
                    error(f"Missing required key '{key}' in k8s service for global k8s upstream {up_name}, file: {filename}, line: {line(s)}")

            if not isinstance(s['k8s_service_port'], int) or not (1 <= s['k8s_service_port'] <= 65535):
                error(f"Invalid k8s_service_port in global k8s upstream {up_name}: {s['k8s_service_port']}, file: {filename}, line: {line(s)}")

            if s['k8s_name'] not in k8s_cluster_names:
                error(f"Invalid k8s_name in global k8s upstream {up_name}: {s['k8s_name']}, file: {filename}, line: {line(s)}")

def convert_k8s_cluster_names(upstreams, k8s_cluster_names):
    for up_name, up in upstreams.items():
        k8s_services = up.get('k8s_services', [])
        for s in k8s_services:
            s['k8s'] = k8s_cluster_names[s['k8s_name']]
    return upstreams

def is_change_global_k8s_upstream(new_up, old_up):
    if new_up.get('ssl', False) != old_up.get('ssl', False):
        return True

    if new_up.get('disable_ssl_verify', False) != old_up.get('disable_ssl_verify', False):
        return True

    if new_up.get('enable_checker', False) != old_up.get('enable_checker', False):
        return True

    if new_up.get('enable_checker', False) is True:
        new_checker = new_up.get('checker', {})
        old_checker = old_up.get('checker', {})
        for key in new_checker:
            if new_checker[key] != old_checker.get(key):
                return True

    new_services = new_up.get('k8s_services', [])
    old_services = old_up.get('k8s_services', [])
    if len(new_services) != len(old_services):
        return True

    for s1, s2 in zip(new_services, old_services):
        if (s1['k8s'] != s2['k8s']
                or s1['k8s_namespace'] != s2['k8s_namespace']
                or s1['k8s_service'] != s2['k8s_service']
                or s1['k8s_service_port'] != s2['k8s_service_port']):
            return True

    return False
