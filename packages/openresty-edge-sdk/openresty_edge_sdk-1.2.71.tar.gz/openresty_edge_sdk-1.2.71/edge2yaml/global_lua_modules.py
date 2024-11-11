import os

from .utils import error, warn, info, md5sum, line
from .read_config import read_lua_modules

def cleanup_global_lua_modules(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    lua_module_sync_to_all = ctx['lua_module_sync_to_all']

    if lua_module_sync_to_all:
        return

    modules = client.get_all_partition_lua_module(partition_id)
    for mod in modules:
        if 'id' in mod:
            try:
                info(f"removing global lua module, partition id: {partition_id}, module id: {mod['id']}")
                client.del_partition_lua_module(partition_id, mod['id'])
            except Exception as e:
                error(f"Failed to partition lua module \"{name}\", lua module id: {mod['id']}", e)

def process_global_lua_modules(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    configs_path = ctx['configs_path']
    lua_module_sync_to_all = ctx['lua_module_sync_to_all']
    location = ctx.get('location', None)

    if not location:
        location = "global_lua_modules"

    # read local lua modules
    new_lua_modules = read_lua_modules(configs_path, location)
    if new_lua_modules is None:
        return

    if not new_lua_modules:
        warn(f"no lua modules were found in directory \"{location}\".")
        if lua_module_sync_to_all:
            # do not delete if sync to all
            return

    info("Checking if lua modules have changed")

    # get old lua module
    old_lua_modules = client.get_all_partition_lua_module(partition_id)
    old_lua_module_names = {}
    # check if lua module changed
    if old_lua_modules:
        for mod in old_lua_modules:
            # print(mod)
            old_lua_module_names[mod['name']] = mod

    # update or insert lua module
    sorted_filenames = sorted(new_lua_modules.keys())
    for mod_name in sorted_filenames:
        mod_code = new_lua_modules[mod_name]
        if mod_name in old_lua_module_names:
            # check md5
            old_mod = old_lua_module_names[mod_name]
            del old_lua_module_names[mod_name]
            if md5sum(mod_code) == md5sum(old_mod['code']):
                # check next module
                # info(f"global lua module have not changed, file: {mod_name}.lua")
                continue
            else:
                # update
                try:
                    info(f"updating global lua module, file: {mod_name}.lua")
                    client.put_partition_lua_module(partition_id, old_mod['id'], mod_name, mod_code)
                except Exception as e:
                    error(f"failed to update global lua module, file: {mod_name}.lua", e)
        else:
            # insert
            try:
                info(f"adding global lua module: {mod_name}.lua")
                client.new_partition_lua_module(partition_id, mod_name, mod_code)
            except Exception as e:
                error(f"failed to add lua module, file: {mod_name}.lua", e)

    if lua_module_sync_to_all:
        # do not delete if sync to all
        return

    for name, mod in old_lua_module_names.items():
        if name not in new_lua_modules:
            try:
                info(f"Removing partition lua module \"{name}\"")
                client.del_partition_lua_module(partition_id, mod['id'])
            except Exception as e:
                error(f"Failed to partition lua module \"{name}\", lua module id: {mod['id']}", e)

def export_global_lua_modules(ctx):
    client = ctx['client']
    partition_id = ctx['partition_id']
    configs_path = ctx['export_to_path']

    modules = client.get_all_partition_lua_module(partition_id)
    if not modules:
        info(f"No global Lua modules found for partition_id: {partition_id}")
        return

    lua_modules_path = os.path.join(configs_path, "global_lua_modules")

    # Create lua_modules directory if it doesn't exist
    os.makedirs(lua_modules_path, exist_ok=True)

    for module in modules:
        module_name = module['name']
        module_code = module['code']

        file_path = os.path.join(lua_modules_path, f"{module_name}.lua")

        try:
            with open(file_path, 'w') as f:
                f.write(module_code)
            info(f"Global Lua module '{module_name}' exported successfully to global_lua_modules/{module_name}.lua")
        except Exception as e:
            error(f"Failed to export global Lua module '{module_name}' to global_lua_modules/{module_name}.lua", e)

    info(f"All global Lua modules exported to global_lua_modules/")
