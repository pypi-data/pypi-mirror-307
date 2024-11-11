import os

from .utils import error, warn, info, generate_certificates, \
    get_app_id_by_domain, line, clear_changes, release_changes
from .read_config import read_yaml_file, write_yaml_config

def add_default_ssl_cert(client, app_id, domains, domain):
    rootCA_key, rootCA_crt, edge_node_key, edge_node_csr, edge_node_crt = generate_certificates(domains, domain)

    client.use_app(app_id)
    client.set_cert_key(cert=edge_node_crt, key=edge_node_key)

def add_http_app(client, partition_id, domains, cn_domain, access_log_name, staging_release):
    domains_str = ",".join(domains)
    info(f"adding http application: {domains_str}, partition id: {partition_id}")
    access_log = dict()
    if access_log_name:
        access_log = {
            'filename': "access.log",
            'name': access_log_name,
        }
    http_ports = [80]
    https_ports = [443]
    partition_ids = [partition_id]

    try:
        app_id = client.new_app(domains=domains, cluster_groups=partition_ids,
                                access_log=access_log, http_ports=http_ports,
                                https_ports=https_ports)
    except Exception as e:
        # just warning, do not interrupt the execution
        warn(f"failed to create app: {e}")

    try:
        info(f"adding ssl cert to app, app id: {app_id}, domain: {domains_str}")
        add_default_ssl_cert(client, app_id, domains, cn_domain)
    except Exception as e:
        # just warning, do not interrupt the execution
        warn(f"failed to ssl cert to app, app id: {app_id}, error: {e}")

    release_changes(client, app_id, staging_release=staging_release)
    return app_id

def process_http_app(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    domain = ctx['domain']
    configs_path = ctx['configs_path']
    staging_release = ctx.get('staging_release', None)

    if not domain:
        error("missing domain.")

    log_format = None
    app_config = None

    file = f"{configs_path}/app.yaml"
    if os.path.exists(file):
        app_config = read_yaml_file(file)

    if app_config and 'access_log_format' in app_config:
        # use the first domain
        log_format = app_config['access_log_format']

    domains = [domain]
    if app_config and 'domains' in app_config:
        app_domains = app_config['domains']
        for dn in app_domains:
            if dn != domain:
                domains.append(dn)

    # get app in partition
    app_id = get_app_id_by_domain(client, partition_id, domain)
    if app_id:
        client.use_app(app_id)

        need_release = False
        if log_format is not None:
            # if this configuration is not specified in the configuration file,
            # then we will not make changes
            data = client.get_app_config(app_id)
            cur_log_format = data.get('access_log', dict())
            cur_log_format_name = cur_log_format.get('name', None)
            if cur_log_format_name is None or cur_log_format_name != log_format:
                try:
                    info(f"updating app config, app id: {app_id}, file: app.yaml, line: {line(app_config)}")
                    new_log_format = {'name': log_format, 'filename': 'access.log'}
                    client.put_app_config(app_id, access_log=new_log_format)
                    need_release = True
                except Exception as e:
                    clear_changes(client, app_id)
                    error(f"failed to update app config, app id: {app_id}, file: app.yaml, line: {line(app_config)}, error: {e}")

        if app_config and 'domains' in app_config:
            # if this configuration is not specified in the configuration file,
            # then we will not make changes
            cur_domains = client.get_app_domains(app_id)
            cur_domains_map = dict()
            for dn in cur_domains:
                cur_domains_map[dn['domain']] = dn

            domain_changed = False
            for dn in domains:
                if dn not in cur_domains_map:
                    # new domain
                    domain_changed = True
                else:
                    del cur_domains_map[dn]

            if cur_domains_map:
                # domain has been removed
                domain_changed = True

            if domain_changed:
                try:
                    app = client.get_app()
                    info(f"updating app domains, app id: {app_id}, file: app.yaml, line: {line(app_config)}")
                    client.put_app(app_id=app_id, domains=domains, label=app.get('name', None))
                    need_release = True
                except Exception as e:
                    clear_changes(client, app_id)
                    error(f"failed to update app domains, app id: {app_id}, file: app.yaml, line: {line(app_config)}, error: {e}")

        if need_release:
            release_changes(client, app_id, staging_release=staging_release)

        ctx['app_id'] = app_id
        return app_id

    staging_release = ctx.get('staging_release', None)
    # app not found, create app
    app_id = add_http_app(client, partition_id, domains, domain, log_format, staging_release)

    ctx['app_id'] = app_id

    return app_id

def cleanup_http_app(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    domain = ctx['domain']

    if not domain:
        warn("without specifying a domain name, the application will not be cleaned")

    # delete app
    app_id = get_app_id_by_domain(client, partition_id, domain)
    if app_id:
        info(f"removing app, app id: {app_id}")
        ok = client.del_app(app_id)
        if not ok:
            raise Exception(f"failed to delete app, app id: {app_id}, domain: {domain}")

def export_app_config(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    domain = ctx['domain']
    configs_path = ctx['export_to_path']

    # get app in partition
    app_id = get_app_id_by_domain(client, partition_id, domain)
    if not app_id:
        ctx['app_not_found'] = True
        warn(f"app not found, app id: {app_id}, domain: {domain}")
        return

    ctx['app_id'] = app_id

    export_data = {}

    # process domains
    domains = client.get_app_domains(app_id)
    if domains:
        export_data['domains'] = [domain['domain'] for domain in domains]

    # process access_log_format
    app_config = client.get_app_config(app_id)
    access_log = app_config.get('access_log', {})
    if access_log and 'name' in access_log:
        export_data['access_log_format'] = access_log['name']

    write_yaml_config(configs_path, "app.yaml", export_data)

    info(f"App configuration exported to app.yaml")
