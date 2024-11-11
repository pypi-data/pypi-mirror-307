# -*- coding: utf-8 -*-

import warnings
import os
import sys
import hashlib
import requests
import argparse
import urllib3
import datetime
import traceback
import socket
from edge2client import Edge2Client
from .utils import error, warn, info, md5sum, cal_config_md5, \
    release_changes, clear_changes, release_partition_changes, \
    clear_partition_changes, line
from .http_app import process_http_app, cleanup_http_app, export_app_config
from .read_config import read_yaml_config, prepare_export_path
from .global_configs import cleanup_global_configs, process_global_configs, \
    export_global_configs
from .upstreams import process_upstreams, cleanup_upstreams, export_upstreams
from .page_rules import process_page_rules, cleanup_page_rules, export_page_rules
from .edgelang_rules import process_edgelang_rules, cleanup_edgelang_rules, export_edgelang_rules
from .global_lua_modules import cleanup_global_lua_modules, \
    process_global_lua_modules, export_global_lua_modules
from .basic_auth_groups import process_basic_auth_groups, export_basic_auth_groups
from .users import process_users, export_users_and_groups
from .edge_email import read_email_configs
from .k8s_upstreams import process_k8s_upstreams, cleanup_k8s_upstreams, export_k8s_upstreams
from .global_upstreams import process_global_upstreams, cleanup_global_upstreams, export_global_upstreams
from .global_k8s_upstreams import process_global_k8s_upstreams, \
    cleanup_global_k8s_upstreams, export_global_k8s_upstreams
from .user_variables import process_user_variables, cleanup_user_variables, export_user_variables
from .ip_lists import process_ip_lists, cleanup_ip_lists, export_ip_lists
from .global_ip_lists import process_global_ip_lists, cleanup_global_ip_lists, export_global_ip_lists
from .waf_whitelist import process_waf_whitelist, cleanup_waf_whitelist, export_waf_whitelist
from .global_custom_actions import process_global_custom_actions, \
    cleanup_global_custom_actions, export_global_custom_actions
from .global_page_templates import process_global_page_templates, \
    cleanup_global_page_templates, export_global_page_templates
from .global_basic_auth_groups import process_global_basic_auth_groups, \
    cleanup_global_basic_auth_groups, export_global_basic_auth_groups
from .global_static_files import process_global_static_files, \
    cleanup_global_static_files, export_global_static_files
from .k8s import process_k8s_clusters, cleanup_k8s_clusters, export_k8s_clusters

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

supported_locations = {
    'page_rules': {
        'process_functions': [ process_http_app, process_page_rules ],
        'cleanup_functions': [ cleanup_page_rules ],
        'export_functions': [ export_page_rules ],
    },
    'edgelang_rules': {
        'process_functions': [ process_http_app, process_edgelang_rules ],
        'cleanup_functions': [ cleanup_edgelang_rules ],
        'export_functions': [ export_edgelang_rules ],
    },
    'upstreams': {
        'process_functions': [ process_http_app, process_upstreams ],
        'cleanup_functions': [ cleanup_upstreams ],
        'export_functions': [ export_upstreams ],
    },
    'k8s_upstreams': {
        'process_functions': [ process_http_app, process_k8s_upstreams ],
        'cleanup_functions': [ cleanup_k8s_upstreams ],
        'export_functions': [ export_k8s_upstreams ],
    },
    'user_variables': {
        'process_functions': [ process_http_app, process_user_variables ],
        'cleanup_functions': [ cleanup_user_variables ],
        'export_functions': [ export_user_variables ],
    },
    'ip_lists': {
        'process_functions': [ process_http_app, process_ip_lists ],
        'cleanup_functions': [ cleanup_ip_lists ],
        'export_functions': [ export_ip_lists ],
    },
    'waf_whitelist': {
        'process_functions': [ process_http_app, process_waf_whitelist ],
        'cleanup_functions': [ cleanup_waf_whitelist ],
        'export_functions': [ export_waf_whitelist ],
    },
    'basic_auth_groups': {
        'process_functions': [ process_http_app, process_basic_auth_groups ],
        'cleanup_functions': [],    # TODO
        'export_functions': [ export_basic_auth_groups ],
    },
    'global_lua_modules': {
        'process_functions': [ process_global_lua_modules ],
        'cleanup_functions': [ cleanup_global_lua_modules ],
        'export_functions': [ export_global_lua_modules ],
        'check_domain': False,
    },
    'global_custom_actions': {
        'process_functions': [ process_global_custom_actions ],
        'cleanup_functions': [ cleanup_global_custom_actions ],
        'export_functions': [ export_global_custom_actions ],
        'check_domain': False,
    },
    'global_configs': {
        'process_functions': [ process_global_configs ],
        'cleanup_functions': [ cleanup_global_configs ],
        'export_functions': [ export_global_configs ],
        'check_domain': False,
    },
    'global_page_templates': {
        'process_functions': [ process_global_page_templates ],
        'cleanup_functions': [ cleanup_global_page_templates ],
        'export_functions': [ export_global_page_templates ],
        'check_domain': False,
    },
    'global_upstreams': {
        'process_functions': [ process_global_upstreams ],
        'cleanup_functions': [ cleanup_global_upstreams ],
        'export_functions': [ export_global_upstreams ],
        'check_domain': False,
    },
    'global_k8s_upstreams': {
        'process_functions': [ process_global_k8s_upstreams ],
        'cleanup_functions': [ cleanup_global_k8s_upstreams ],
        'export_functions': [ export_global_k8s_upstreams ],
        'check_domain': False,
    },
    'global_ip_lists': {
        'process_functions': [ process_global_ip_lists ],
        'cleanup_functions': [ cleanup_global_ip_lists ],
        'export_functions': [ export_global_ip_lists ],
        'check_domain': False,
    },
    'global_basic_auth_groups': {
        'process_functions': [ process_global_basic_auth_groups ],
        'cleanup_functions': [ cleanup_global_basic_auth_groups ],
        'export_functions': [ export_global_basic_auth_groups ],
        'check_domain': False,
    },
    'global_static_files': {
        'process_functions': [ process_global_static_files ],
        'cleanup_functions': [ cleanup_global_static_files ],
        'export_functions': [ export_global_static_files ],
        'check_domain': False,
    },
    'k8s': {
        'process_functions': [ process_k8s_clusters ],
        'cleanup_functions': [ cleanup_k8s_clusters ],
        'export_functions': [ export_k8s_clusters ],
        'check_domain': False,
    },
    'users': {
        'process_functions': [ process_users ],
        'cleanup_functions': [],    # do not support
        'export_functions': [ export_users_and_groups ],
        'check_domain': False,
    },
    'all': {
        'process_functions': [
            process_k8s_clusters,
            process_global_configs,
            process_global_lua_modules,
            process_global_basic_auth_groups,
            process_global_upstreams,
            process_global_k8s_upstreams,
            process_global_ip_lists,
            process_global_page_templates,
            process_global_static_files,
            process_global_custom_actions,
            process_http_app,
            # TODO add/update before updating page rules, delete after page rules
            process_upstreams,
            process_k8s_upstreams,
            process_basic_auth_groups,
            process_user_variables,
            process_ip_lists,
            process_waf_whitelist,
            process_edgelang_rules,
            process_page_rules,
            process_users,
        ],
        'cleanup_functions': [
            cleanup_page_rules,     # for compatibility with older versions(<24.9.1) of Edge.
            cleanup_http_app,
            cleanup_global_configs,
            cleanup_global_lua_modules,
            cleanup_global_custom_actions,
            cleanup_global_basic_auth_groups,
            cleanup_global_upstreams,
            cleanup_global_k8s_upstreams,
            cleanup_global_ip_lists,
            cleanup_global_page_templates,
            cleanup_global_static_files,
            cleanup_k8s_clusters,
        ],
        'export_functions': [
            export_app_config,
            export_page_rules,
            export_edgelang_rules,
            export_upstreams,
            export_k8s_upstreams,
            export_user_variables,
            export_ip_lists,
            export_waf_whitelist,
            # NOTE: do not export basic auth users by default
            export_basic_auth_groups,
            export_global_basic_auth_groups,
            export_global_custom_actions,
            export_global_lua_modules,
            export_global_upstreams,
            export_global_k8s_upstreams,
            export_global_ip_lists,
            export_global_page_templates,
            export_global_configs,
            export_global_static_files,
            export_k8s_clusters,
            export_users_and_groups,
        ],
    },
}

def parse_args():
    description = "Update or add OpenResty Edge configuration."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-t", "--api-token", dest="api_token", action="store", required=True,
                        help="specify the API token for sending the request")
    parser.add_argument("-u", "--admin-url", dest="admin_url", action="store", required=True,
                        help="specify the URL of the OpenResty Edge Admin. For example, https://admin.com:443")
    parser.add_argument("-s", "--disable-ssl-verify", dest="disable_ssl_verify", action="store_true", default=False,
                        help="turn off SSL verification for requests to access OpenResty Edge Admin")
    parser.add_argument("-i", "--configs-path", dest="configs_path", action="store", required=False,
                        help="specify the path to the configuration file")
    parser.add_argument("-e", "--email-config-file", dest="email_config_file", action="store", required=False,
                        help="specify the file to the email configuration; if not specified, the email.yaml file in the configuration path will be used")
    parser.add_argument("-U", "--users-config-path", dest="users_config_path", action="store", required=False,
                        help="specify the path to the users configuration; if not specified, the users/ path in the configuration path will be used")
    parser.add_argument("-F", "--export-fake-privacy-info", dest="export_fake_info", action="store_true", required=False,
                        help="use placeholders in place of privacy information when exporting")
    parser.add_argument("-S", "--staging-release", dest="staging_release", action="store_true", default=False,
                        help="only release the configuration to the staging gateway server")

    keys_string = ', '.join(supported_locations.keys())
    parser.add_argument("-l", "--location", dest="location", action="store",
                        help=f"specify the configuration name that needs to be updated, supported: {keys_string}")
    parser.add_argument("-d", "--domain", dest="domain", action="store",
                        help="specify a domain name. When an HTTP application containing this domain exists, it will be updated; otherwise, a new application will be created")
    parser.add_argument("-P", "--export-to-path", dest="export_to_path", action="store",
                        help="specify the storage path of the exported configuration. If not specified, a directory prefixed with configs will be automatically created in the current path.")


    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("-p", "--partition-id", dest="partition_id", action="store", type=int,
                        help="specify the id of the partition where you want to add or update the configuration")
    group.add_argument("-n", "--partition-name", dest="partition_name", action="store",
                        help="specify the name of the partition where you want to add or update the configuration")

    action_group = parser.add_mutually_exclusive_group(required=False)
    action_group.add_argument("-c", "--cleanup", dest="cleanup", action="store_true", default=False,
                        help="based on the location. This option allows for the cleanup of page rules, application upstreams, global user variables, and resetting the access log format for partitions. It can also be used independently of the location")
    action_group.add_argument("-E", "--export", dest="export", action="store_true", default=False,
                        help="export the configuration to the specified path, which can be specified through the --export-to-path option")

    args = parser.parse_args()

    location = args.location
    if location is not None and location not in supported_locations:
        parser.error(f"unsupported location: {location}.\n\nAvaiable locations:\n{keys_string}")

    ssl_verify = True
    if args.disable_ssl_verify is True:
        ssl_verify = False
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        requests.packages.urllib3.disable_warnings()

    client = Edge2Client(args.admin_url, None, None, args.api_token)
    client.set_ssl_verify(ssl_verify)

    data = client.get_sync_to_all()
    if not client.request_ok():
        error("Failed to get sync to all flag from OpenResty Edge Admin")

    ngx_sync_to_all = data.get('ngx', True) if data else True
    lua_module_sync_to_all = data.get('lua_module', True) if data else True

    check_users_only = False
    if (location is not None and location == "users") \
    and (args.users_config_path is not None):
        check_users_only = True
    else:
        if not args.export and not args.cleanup:
            configs_path = args.configs_path
            if configs_path is None:
                parser.error("the following arguments are required: -i/--configs-path")

            if not os.path.exists(configs_path):
                error(f"configs path not exists: {configs_path}")

            if not os.path.isdir(configs_path):
                error(f"configs path is not a directory: {configs_path}")

        if not ngx_sync_to_all or not lua_module_sync_to_all:
            if args.partition_id is None and args.partition_name is None:
                parser.error("the following arguments are required: -p/--partition-id or -n/--partition-name")

        if not (location is not None and supported_locations[location].get('check_domain', True) is False) and args.domain is None:
            parser.error("the following arguments are required: -d/--domain")

    email_config_file = args.email_config_file
    if email_config_file and not os.path.exists(email_config_file):
        error(f"sender's email config file not exists: {email_config_file}")

    users_config_path = args.users_config_path
    if users_config_path and not os.path.exists(users_config_path):
        error(f"users config path not exists: {users_config_path}")

    staging_release = False
    if args.staging_release:
        staging_release = True

    return {
        'args': args,
        'check_users_only': check_users_only,
        'client': client,
        'ngx_sync_to_all': ngx_sync_to_all,
        'lua_module_sync_to_all': lua_module_sync_to_all,
        'export_fake_info': args.export_fake_info,
        'staging_release': staging_release
    }

def cleanup(ctx):
    location = ctx['location']
    if not location:
        location = "all"

    export_functions = supported_locations[location]['cleanup_functions']

    for func in export_functions:
        try:
            func(ctx)
        except Exception as e:
            error(f"failed to cleanup", e)

def export(ctx):
    location = ctx['location']
    if not location:
        location = "all"
        ctx['export_users'] = False
    else:
        ctx['export_users'] = True

    export_functions = supported_locations[location]['export_functions']

    for func in export_functions:
        try:
            func(ctx)
        except Exception as e:
            error(f"failed to export", e)

def import_to_edge(ctx):
    location = ctx['location']
    if not location:
        location = "all"

    export_functions = supported_locations[location]['process_functions']

    for func in export_functions:
        try:
            func(ctx)
        except Exception as e:
            error(f"failed to import", e)

def check_partition(client, partition_id, partition_name):
    if partition_id:
        data = client.get_cluster_group(partition_id)
        if not data:
            error(f'partition not found, partition id: {partition_id}')

        return partition_id

    if partition_name:
        partitions = client.get_all_cluster_groups()
        for p in partitions:
            if p['name'] == partition_name:
                # get partition_id
                return p['id']

        error(f'partition not found, partition name: {partition_name}')

def main(args=None):
    ctx = parse_args()

    args = ctx['args']
    check_users_only = ctx['check_users_only']
    client = ctx['client']
    ngx_sync_to_all = ctx['ngx_sync_to_all']

    versions = client.get_version()
    if versions is None or versions.get('product_type', None) is None:
        error("get openresty edge product type failed")

    if versions['product_type'] != 'enterprise':
        error("openresty edge product type is not enterprise")

    location = args.location
    configs_path = args.configs_path

    ctx['location'] = location
    ctx['configs_path'] = configs_path

    email_config_file = args.email_config_file
    if email_config_file is None and configs_path is not None:
        email_config_file = f"{configs_path}/email.yaml"

    users_config_path = args.users_config_path
    if users_config_path is None and configs_path is not None:
        users_config_path = f"{configs_path}/users"

    ctx['users_config_path'] = users_config_path

    email_configs = read_email_configs(email_config_file)

    ctx['email_configs'] = email_configs

    if ngx_sync_to_all is False:
        partition_id = args.partition_id
        partition_name = args.partition_name
        if check_users_only != True:
            partition_id = check_partition(client, partition_id, partition_name)
    else:
        # default partition is 1
        partition_id = 1
        partition_name = "default"

    ctx['partition_id'] = partition_id
    ctx['partition_name'] = partition_name

    domain = args.domain
    ctx['domain'] = domain

    if args.export:
        export_configs_path = args.export_to_path
        if export_configs_path is None:
            export_configs_path = prepare_export_path(partition_id, domain)
            info(f"export configs path: {export_configs_path}")

        ctx['export_to_path'] = export_configs_path

        export(ctx)
        print("[!] Export Finished.")
        sys.exit()

    if args.cleanup:
        cleanup(ctx)
        print("[!] Cleanup Finished.")
        sys.exit()

    import_to_edge(ctx)
    print("[!] Import Finished.")

if __name__ == "__main__":
    exit(main())
