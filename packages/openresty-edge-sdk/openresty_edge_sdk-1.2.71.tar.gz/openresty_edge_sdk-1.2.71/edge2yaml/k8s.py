import os

from .utils import error, warn, info, fix_line, is_valid_host, \
    is_valid_ipv4_address, is_valid_ipv6_address
from .read_config import read_yaml_config, write_yaml_config, add_before_comment

def check_k8s_clusters(clusters, filename):
    if not isinstance(clusters, list):
        error(f"Unsupported K8s clusters file format, file: {filename}")

    names = dict()
    for cluster in clusters:
        if not isinstance(cluster, dict):
            error(f"Each K8s cluster must be a dictionary, file: {filename}, line: {fix_line(cluster.lc.line)}")

        required_fields = ['name', 'host', 'port', 'token']
        for field in required_fields:
            if field not in cluster:
                error(f"Missing required field '{field}' in K8s cluster, file: {filename}, line: {fix_line(cluster.lc.line)}")

        if cluster['name'] in names:
            error(f"Duplicate name in K8s cluster {cluster['name']}, file: {filename}, line: {fix_line(cluster.lc.line)}")

        names[cluster['name']] = True

        if not is_valid_host(cluster['host']):
            error(f"Invalid host in K8s cluster {cluster['name']}: {cluster['host']}, file: {filename}, line: {fix_line(cluster.lc.line)}")

        if not isinstance(cluster['port'], int) or not (1 <= cluster['port'] <= 65535):
            error(f"Invalid port in K8s cluster {cluster['name']}: {cluster['port']}, file: {filename}, line: {fix_line(cluster.lc.line)}")

        if not isinstance(cluster['token'], str) or not cluster['token']:
            error(f"Invalid token in K8s cluster {cluster['name']}, file: {filename}, line: {fix_line(cluster.lc.line)}")

        if 'ssl_verify' in cluster and not isinstance(cluster['ssl_verify'], bool):
            error(f"Invalid ssl_verify in K8s cluster {cluster['name']}, file: {filename}, line: {fix_line(cluster.lc.line)}")

        for timeout in ['connect_timeout', 'read_timeout', 'send_timeout']:
            if timeout in cluster and not isinstance(cluster[timeout], int):
                error(f"Invalid {timeout} in K8s cluster {cluster['name']}, file: {filename}, line: {fix_line(cluster.lc.line)}")

    return True

def is_change_k8s_cluster(new_cluster, old_cluster):
    fields_to_compare = [
        'host',
        'port',
        'domain',
        'ssl_verify',
        'connect_timeout',
        'read_timeout',
        'send_timeout',
        'token'
    ]
    return any(new_cluster.get(field) != old_cluster.get(field) for field in fields_to_compare)

def process_k8s_clusters(ctx):
    client = ctx['client']
    configs_path = ctx['configs_path']
    location = ctx.get('location', None)

    if not location:
        location = "k8s"

    configs = read_yaml_config(configs_path, location)
    if configs is None:
        return

    info("Checking if K8s clusters are valid")
    for filename, clusters in configs.items():
        check_k8s_clusters(clusters, filename)

    old_clusters = client.get_all_global_k8s()

    old_clusters_dict = {cluster['name']: cluster for cluster in old_clusters}

    info("Checking if K8s clusters have changed")
    new_clusters_dict = {}
    sorted_configs = sorted(configs.keys())

    for filename in sorted_configs:
        clusters = configs[filename]
        for cluster in clusters:
            new_clusters_dict[cluster['name']] = True

            host = None
            domain = None
            if is_valid_ipv4_address(cluster['host']) or is_valid_ipv6_address(cluster['host']):
                host = cluster['host']
            else:
                domain = cluster['host']

            if cluster['name'] in old_clusters_dict:
                old_cluster = old_clusters_dict[cluster['name']]
                if is_change_k8s_cluster(cluster, old_cluster):
                    try:
                        info(f"Updating K8s cluster \"{cluster['name']}\"")
                        client.put_global_k8s(
                            k8s_id=old_cluster['id'],
                            name=cluster['name'],
                            host=host,
                            domain=domain,
                            port=cluster['port'],
                            ssl_verify=cluster.get('ssl_verify', False),
                            connect_timeout=cluster.get('connect_timeout', 15),
                            read_timeout=cluster.get('read_timeout', 15),
                            send_timeout=cluster.get('send_timeout', 15),
                            token=cluster['token']
                        )
                    except Exception as e:
                        error(f"Failed to update K8s cluster, file: {filename}, line: {fix_line(cluster.lc.line)}", e)
            else:
                try:
                    info(f"Adding K8s cluster \"{cluster['name']}\"")
                    client.new_global_k8s(
                        name=cluster['name'],
                        host=host,
                        domain=domain,
                        port=cluster['port'],
                        ssl_verify=cluster.get('ssl_verify', False),
                        connect_timeout=cluster.get('connect_timeout', 30),
                        read_timeout=cluster.get('read_timeout', 30),
                        send_timeout=cluster.get('send_timeout', 30),
                        token=cluster['token']
                    )
                except Exception as e:
                    error(f"Failed to add K8s cluster, file: {filename}, line: {fix_line(cluster.lc.line)}", e)

    # for cluster_name, cluster in old_clusters_dict.items():
    #     if cluster_name not in new_clusters_dict:
    #         try:
    #             info(f"Removing K8s Endpoint in K8s cluster \"{cluster_name}\"")
    #             client.del_k8s_endpoints(cluster['id'])
    #             info(f"Removing K8s cluster \"{cluster_name}\"")
    #             client.del_global_k8s(cluster['id'])
    #         except Exception as e:
    #             error(f"Failed to remove K8s cluster, cluster id: {cluster['id']}", e)

def cleanup_k8s_clusters(ctx):
    pass
    # client = ctx['client']

    # clusters = client.get_all_global_k8s()

    # for cluster in clusters:
    #     try:
    #         info(f"Removing K8s Endpoint in K8s cluster \"{cluster['name']}\"")
    #         client.del_k8s_endpoints(cluster['id'])
    #         info(f"Removing K8s cluster \"{cluster['name']}\"")
    #         client.del_global_k8s(cluster['id'])
    #     except Exception as e:
    #         error(f"Failed to remove K8s cluster, cluster id: {cluster['id']}", e)

def export_k8s_clusters(ctx):
    client = ctx['client']
    configs_path = ctx['export_to_path']

    clusters = client.get_all_global_k8s()

    if not clusters:
        info(f"No K8s clusters found")
        return

    formatted_clusters = []
    for cluster in clusters:
        host = cluster.get('host', None)
        if host is None:
            host = cluster.get('domain', None)

        token = ''
        if ctx['export_fake_info']:
            token = "********"

        formatted_cluster = {
            'name': cluster['name'],
            'host': host,
            'port': cluster['port'],
            'ssl_verify': cluster.get('ssl_verify', False),
            'connect_timeout': cluster.get('connect_timeout', 15),
            'read_timeout': cluster.get('read_timeout', 15),
            'send_timeout': cluster.get('send_timeout', 15),
            'token': token,
        }

        formatted_cluster = add_before_comment(formatted_cluster, 'token',
                                                "token: We don't export actual token for security reasons")

        formatted_clusters.append(formatted_cluster)

    export_path = os.path.join(configs_path, "k8s")

    try:
        write_yaml_config(export_path, "k8s.yaml", formatted_clusters)
        info(f"K8s clusters exported successfully to k8s/k8s.yaml")
    except Exception as e:
        error(f"Failed to export K8s clusters to k8s/k8s.yaml", e)
