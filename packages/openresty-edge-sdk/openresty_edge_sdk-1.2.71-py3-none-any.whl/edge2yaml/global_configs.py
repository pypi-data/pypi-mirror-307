import json
import os

from .utils import error, warn, info, line, get_updated_list, to_fake_name, \
    clear_partition_changes, release_partition_changes, to_real_name
from .read_config import read_yaml_config, write_yaml_config
from .global_variables import replace_global_variable_in_log_formats, \
    restore_global_variable_names_in_log_formats

def reset_access_log_format(client, partition_id):
    partition_ngx_conf = client.get_partition_ngx_config(partition_id, detail=True)
    if 'access_log_formats' not in partition_ngx_conf:
        error(f"access log formats not found in Edge Admin, partition id: {partition_id}")

    main_id = None
    for fmt in partition_ngx_conf['access_log_formats']:
        if fmt.get('name', False) == "main":
            main_id = fmt['id']

    config = dict()
    config['access_log_formats'] = [
        {
            'id': main_id,
            'name': "main",
            'default': True,
            'format': "$remote_addr - $remote_user [$time_local] $http_host \"$request\" $status $body_bytes_sent $request_time \"$http_referer\" \"$http_user_agent\" $upstream_addr $upstream_status $upstream_response_time",
        }];

    try:
        info(f"reset access log format, partition id: {partition_id}")
        client.set_partition_ngx_config(config, partition_id)
    except Exception as e:
        clear_partition_changes(client, partition_id)
        error(f"failed to reset access log formats, partition id: {partition_id}", e)

    # release partition changes
    release_partition_changes(client, partition_id)

def read_global_config(configs_path, location, config_key=None):
    global_configs = read_yaml_config(configs_path, location)
    if global_configs is not None:
        filename = f"{location}.yaml"
        configs = global_configs[filename]
        if config_key is not None:
            target_config = configs.get(config_key, None)
            return target_config
        else:
            return configs

    return None

def read_access_log_formats(configs_path, location):
    new_formats = dict()
    found_default = False
    new_format_list = read_global_config(configs_path, location, "access_log_formats")
    if new_format_list is None:
        return new_formats, found_default

    for fmt in new_format_list:
        if 'name' not in fmt:
            error(f"missing name of access log format, file: {fmt.lc.filename}, line:{line(fmt)}")
        if 'format' not in fmt:
            error(f"missing format of access log format, file: {fmt.lc.filename}, line:{line(fmt)}")

        fmt['format'] = fmt['format'].replace("\n", "")
        if 'escape' in fmt and fmt['escape'] == "json":
            try:
                fmt['format'] = json.dumps(json.loads(fmt['format']))
            except:
                error(f"invalid access log format, unable to minimize json format, file: {fmt.lc.filename}, line:{line(fmt)}")

        # check if multiple default formats
        if fmt.get('default', False) == True:
            if found_default == True:
                error(f"multiple default access log formats, file: {fmt.lc.filename}, line:{line(fmt)}")
            else:
                found_default = True

        new_formats[fmt['name']] = fmt

    return new_formats, found_default

def read_global_custom_shared_zone(configs_path, location):
    zones = dict()
    zones_list = read_global_config(configs_path, location, "custom_shared_zone")
    if zones_list is None:
        return zones

    for v in zones_list:
        if 'name' not in v:
            error(f"missing name of access log format, file: {v.lc.filename}, line: {line(v)}")

        zones[v['name']] = v

    return zones

def read_global_user_variables(configs_path, location, partition_id):
    variables = dict()
    variables_list = read_global_config(configs_path, location, "user_variables")
    if variables_list is None:
        return variables

    for v in variables_list:
        if 'name' not in v:
            error(f"missing name of access log format, file: {v.lc.filename}, line: {line(v)}")

        var_name = v['name']
        variables[var_name] = v

    return variables

def process_global_configs(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    configs_path = ctx['configs_path']
    location = ctx.get('location', None)

    if not location:
        location = "global_configs"

    configs = read_yaml_config(configs_path, location)
    if configs is None:
        return

    # 1. process global variables
    info("Checking if global user variables have changed")
    new_variables = read_global_user_variables(configs_path, location, partition_id)
    if new_variables:
        old_variable_list = client.get_all_global_vars()
        updated_list = get_updated_list(new_variables, old_variable_list,
                                        "name", ["default", "type"], True)
        if updated_list:
            for var in updated_list:
                if 'id' in var:
                    try:
                        info(f"updating global user variable, variable id: {var['id']}, variable name: {var['name']}")
                        client.put_global_var(var_id=var['id'], name=var['name'],
                                        var_type=var['type'], default=var['default'])
                    except Exception as e:
                        error(f"failed to update global user variable", e)
                else:
                    try:
                        info(f"adding global user variable: {var['name']}")
                        client.new_global_var(name=var['name'], var_type=var['type'], default=var['default'])
                    except Exception as e:
                        error(f"failed to add global user variable", e)
    else:
        info("user variables not found in global_configs.yaml, skipping user variables...")

    # 2. process access log formats
    info("Checking if access log formats have changed")
    new_formats, found_default = read_access_log_formats(configs_path, location)
    if new_formats:
        # found log format in global_configs.yaml
        replace_global_variable_in_log_formats(client, new_formats,
                                            location + ".yaml", partition_id)
        partition_ngx_conf = client.get_partition_ngx_config(partition_id, detail=True)
        if 'access_log_formats' not in partition_ngx_conf:
            error(f"access log formats not found in Edge Admin, partition id: {partition_id}")

        if found_default:
            for fmt in partition_ngx_conf['access_log_formats']:
                if fmt.get('default', False) == True:
                    fmt['default'] = False

        # check if access log changed
        updated_list = get_updated_list(new_formats,
                                        partition_ngx_conf['access_log_formats'],
                                        "name",
                                        ["format", "escape", "default"])

        # update if change
        if updated_list:
            new_config = {
                'access_log_formats': updated_list
            }
            try:
                info(f"updating access log formats, partition id: {partition_id}")
                client.set_partition_ngx_config(new_config, partition_id)
            except Exception as e:
                clear_partition_changes(client, partition_id)
                error(f"failed to update access log formats, partition id: {partition_id}", e)
    else:
        info("access log formats not found in global_configs.yaml, skipping log format...")

    # release partition changes
    release_partition_changes(client, partition_id)

    # 3. process custom shared zone
    info("Checking if custom shared zones have changed")
    new_zones = read_global_custom_shared_zone(configs_path, location)
    if new_zones:
        global_ngx_conf = client.get_global_ngx_config(detail=True)

        old_shared_zone = list()
        if 'custom_shared_zone' in global_ngx_conf:
            old_shared_zone = global_ngx_conf['custom_shared_zone']

        updated_list = get_updated_list(new_zones,
                                        old_shared_zone,
                                        "name",
                                        ["size_unit", "size"])

        # update if change
        if updated_list:
            info("updating custom shared zone...")
            new_config = {
                'custom_shared_zone': updated_list
            }
            # global_ngx_conf['custom_shared_zone'] = updated_list
            client.set_global_ngx_config(new_config)
    else:
        info("custom shared zones not found in global_configs.yaml, skipping shared zones...")


def cleanup_global_configs(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    ngx_sync_to_all = ctx['ngx_sync_to_all']

    if ngx_sync_to_all:
        return

    # reset access log
    reset_access_log_format(client, partition_id)
    # do not delete global variables, supporting updates and inserts is enough
    release_partition_changes(client, partition_id)
    # do not delete custom shared zone
    # TODO check if custom shared zone using in global lua module (all partitions)

def export_global_configs(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    configs_path = ctx['export_to_path']

    global_configs = {}

    # 1. Export user variables
    info("Exporting global user variables...")
    user_variables = client.get_all_global_vars()
    if user_variables:
        new_variables = list()
        for v in user_variables:
            name = v['name']

            # name == None means that the global variable does not belong to this partition
            if name is not None:
                new_v = {
                    'name': name,
                    'type': v.get('type', 'string'),
                    'default': v.get('default', '-'),
                }
                new_variables.append(new_v)

        global_configs['user_variables'] = new_variables

    # 2. Export access log formats
    info("Exporting global access log formats...")
    partition_ngx_conf = client.get_partition_ngx_config(partition_id, detail=True)
    if 'access_log_formats' in partition_ngx_conf:
        # replace global variable id to variable name
        formats = partition_ngx_conf['access_log_formats']
        global_configs['access_log_formats'] = restore_global_variable_names_in_log_formats(client, formats, partition_id)

    # 3. Export custom shared zones
    info("Exporting global custom shared zones...")
    global_ngx_conf = client.get_global_ngx_config(detail=True)
    if 'custom_shared_zone' in global_ngx_conf:
        global_configs['custom_shared_zone'] = global_ngx_conf['custom_shared_zone']

    export_path = configs_path

    # Write to YAML file
    try:
        write_yaml_config(export_path, "global_configs.yaml", global_configs)
        info(f"Global configs exported successfully to global_configs.yaml")
    except Exception as e:
        error(f"Failed to export global configs to global_configs.yaml", e)
