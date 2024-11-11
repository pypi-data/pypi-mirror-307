import os

from .utils import error, warn, info, get_app_id_by_domain, release_changes, \
    clear_changes, line
from .read_config import read_yaml_config, write_yaml_config

def check_upstream_checker(up, up_name, filename):
    enable_checker = up.get('enable_checker', False)
    if not isinstance(enable_checker, bool):
        error(f"enable_checker flag for k8s upstream {up_name} must be a boolean, file: {filename}, line: {up.lc.line}")

    if enable_checker:
        checker = up.get('checker', dict())
        if not isinstance(checker, dict):
            error(f"checker for k8s upstream {up_name} must be a dict, file: {filename}, line: {checker.lc.line}")

        # Check required fields for checker
        required_checker_fields = ['type', 'interval', 'timeout', 'fall', 'rise']
        for field in required_checker_fields:
            if field not in checker:
                error(f"Missing required checker field '{field}' for k8s upstream {up_name}, file: {filename}, line: {checker.lc.line}")

        # Check types and values for specific fields
        if checker['type'] not in ['http', 'https', 'tcp', 'mysql', 'postgresql']:
            error(f"Invalid checker type for k8s upstream {up_name}, file: {filename}, line: {checker.lc.line}")

        for field in ['interval', 'timeout', 'fall', 'rise']:
            if not isinstance(checker[field], int) or checker[field] <= 0:
                error(f"Invalid {field} value for checker in k8s upstream {up_name}, file: {filename}, line: {checker.lc.line}")

        # Check optional fields
        if 'http_req_method' in checker and checker['http_req_method'] not in ['GET', 'HEAD']:
            error(f"Invalid http_req_method for checker in k8s upstream {up_name}, file: {filename}, line: {checker.lc.line}")

        if 'valid_statuses' in checker:
            if not isinstance(checker['valid_statuses'], list) or not all(status in [200, 301, 302] for status in checker['valid_statuses']):
                error(f"Invalid valid_statuses for checker in k8s upstream {up_name}, file: {filename}, line: {checker.lc.line}")

def check_k8s_upstreams(upstreams, filename, k8s_cluster_names):
    if not isinstance(upstreams, dict):
        error(f"Unsupported k8s upstream file format, file: {filename}")

    names = dict()
    for up_name, up in upstreams.items():
        if up_name in names:
            error(f"Duplicate name in upstream {up_name}, file: {filename}, line: {line(up)}")

        names[up_name] = True

        if not isinstance(up, dict):
            error(f"K8s upstream for name {up_name} must be a dict, file: {filename}, line: {line(up)}")

        ssl = up.get('ssl', False)
        if not isinstance(ssl, bool):
            error(f"ssl flag for k8s upstream {up_name} must be a boolean, file: {filename}, line: {line(ssl)}")

        disable_ssl_verify = up.get('disable_ssl_verify', False)
        if not isinstance(disable_ssl_verify, bool):
            error(f"disable_ssl_verify flag for k8s upstream {up_name} must be a boolean, file: {filename}, line: {line(disable_ssl_verify)}")

        check_upstream_checker(up, up_name, filename)

        k8s_services = up.get('k8s_services', None)
        if not isinstance(k8s_services, list) or not all(isinstance(item, dict) for item in k8s_services):
            error(f"k8s_services for upstream {up_name} must be a list of dictionaries, file: {filename}, line: {line(k8s_services)}")

        for s in k8s_services:
            required_keys = ['k8s_name', 'k8s_namespace', 'k8s_service', 'k8s_service_port']
            for key in required_keys:
                if key not in s:
                    error(f"Missing required key '{key}' in k8s service for upstream {up_name}, file: {filename}, line: {line(s)}")

            if not isinstance(s['k8s_service_port'], int) or not (1 <= s['k8s_service_port'] <= 65535):
                error(f"Invalid k8s_service_port in upstream {up_name}: {s['k8s_service_port']}, file: {filename}, line: {line(s)}")

            if s['k8s_name'] not in k8s_cluster_names:
                error(f"Invalid k8s_name in upstream {up_name}: {s['k8s_name']}, file: {filename}, line: {line(s)}")

    return True

def convert_k8s_cluster_names(upstreams, k8s_cluster_names):
    for up_name, up in upstreams.items():
        k8s_services = up.get('k8s_services', list())
        for s in k8s_services:
            s['k8s'] = k8s_cluster_names[s['k8s_name']]

    return upstreams

def is_change_k8s_upstream(new_up, old_up):
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

    new_services = new_up.get('k8s_services', list())
    old_services = old_up.get('k8s_services', list())
    if len(new_services) != len(old_services):
        return True

    for s1, s2 in zip(new_services, old_services):
        if (s1['k8s'] != s2['k8s']
                or s1['k8s_namespace'] != s2['k8s_namespace']
                or s1['k8s_service'] != s2['k8s_service']
                or s1['k8s_service_port'] != s2['k8s_service_port']):

            return True

    # no change
    return False

def process_k8s_upstreams(ctx):
    client = ctx['client']
    app_id = ctx['app_id']
    configs_path = ctx['configs_path']
    location = ctx.get('location', None)
    staging_release = ctx.get('staging_release', None)

    if not location:
        location = "k8s_upstreams"

    configs = read_yaml_config(configs_path, location)
    if configs is None:
        return

    k8s_clusters = client.get_all_global_k8s()
    k8s_cluster_names = dict()
    for cluster in k8s_clusters:
        k8s_cluster_names[cluster['name']] = cluster['id']

    info("Checking if k8s upstream is valid")
    for filename, ups in configs.items():
        check_k8s_upstreams(ups, filename, k8s_cluster_names)

    ups = convert_k8s_cluster_names(ups, k8s_cluster_names)

    client.use_app(app_id)
    old_upstreams = client.get_all_k8s_upstreams(detail=True, with_service=True)

    old_upstream_dict = {up['name']: up for up in old_upstreams}

    info("Checking if k8s upstream have changed")
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
                if is_change_k8s_upstream(new_up, old_up):
                    try:
                        info(f"Updating k8s upstream \"{up_name}\", app id: {app_id}")
                        client.put_k8s_upstream(
                            up_id=old_up['id'],
                            name=up_name,
                            k8s_services=new_up['k8s_services'],
                            ssl=new_up.get('ssl', False),
                            disable_ssl_verify=new_up.get('disable_ssl_verify', False),
                            health_checker=checker,
                        )
                    except Exception as e:
                        clear_changes(client, app_id)
                        error(f"Failed to update k8s upstream, file: {filename}, line: {line(new_up)}", e)
            else:
                try:
                    info(f"Adding k8s upstream \"{up_name}\" to app, app id: {app_id}")
                    client.new_k8s_upstream(
                        name=up_name,
                        k8s_services=new_up['k8s_services'],
                        ssl=new_up.get('ssl', False),
                        disable_ssl_verify=new_up.get('disable_ssl_verify', False),
                        health_checker=checker
                    )
                except Exception as e:
                    clear_changes(client, app_id)
                    error(f"Failed to add k8s upstream to app, file: {filename}, line: {line(new_up)}", e)

    for up_name, up in old_upstream_dict.items():
        if up_name not in new_upstream_dict:
            try:
                info(f"Removing k8s upstream \"{up_name}\" from app, app id: {app_id}")
                client.del_k8s_upstream(up['id'])
            except Exception as e:
                clear_changes(client, app_id)
                error(f"Failed to remove k8s upstream from app, app id: {app_id}, upstream id: {up['id']}", e)

    release_changes(client, app_id, staging_release=staging_release)

def cleanup_k8s_upstreams(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    domain = ctx['domain']
    staging_release = ctx.get('staging_release', None)

    app_id = get_app_id_by_domain(client, partition_id, domain)
    if not app_id:
        error(f"App not found, app id: {app_id}, domain: {domain}")

    client.use_app(app_id)
    k8s_upstreams = client.get_all_k8s_upstreams(detail=False)

    for up_name, up_id in k8s_upstreams.items():
        try:
            info(f"Removing k8s upstream \"{up_name}\"(id: {up_id}) from app, app id: {app_id}")
            client.del_k8s_upstream(up_id)
        except Exception as e:
            clear_changes(client, app_id)
            error(f"Failed to remove k8s upstream from app, app id: {app_id}, upstream: {up_name}(id: {up_id})", e)

    release_changes(client, app_id, staging_release=staging_release)

def export_k8s_upstreams(ctx):
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
    k8s_upstreams = client.get_all_k8s_upstreams(detail=True, with_service=True)

    if not k8s_upstreams:
        info(f"No k8s upstreams found for app_id: {app_id}")
        return

    k8s_clusters = client.get_all_global_k8s()
    k8s_cluster_ids = dict()
    for cluster in k8s_clusters:
        k8s_cluster_ids[cluster['id']] = cluster['name']

    formatted_upstreams = {}
    for upstream in k8s_upstreams:
        upstream_name = upstream['name']
        k8s_services = upstream.get('k8s_services', list())
        new_k8s_services = list()
        for service in k8s_services:
            k8s_name = k8s_cluster_ids.get(service['k8s'], None)
            if k8s_name is None:
                error("k8s cluster not found, k8s id: {service['k8s']}")

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
            formatted_upstream['checker'] = upstream.get('checker', dict())

        formatted_upstreams[upstream_name] = formatted_upstream

    export_path = os.path.join(configs_path, "k8s_upstreams")

    try:
        write_yaml_config(export_path, "k8s_upstreams.yaml", formatted_upstreams)
        info(f"K8s upstreams exported successfully to k8s_upstreams/k8s_upstreams.yaml")
    except Exception as e:
        error(f"Failed to export k8s upstreams to k8s_upstreams/k8s_upstreams.yaml", e)
