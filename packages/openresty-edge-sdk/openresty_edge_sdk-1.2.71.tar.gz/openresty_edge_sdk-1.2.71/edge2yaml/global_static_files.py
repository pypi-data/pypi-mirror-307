import os
import hashlib

from .utils import error, warn, info, line
from .read_config import read_yaml_config, write_yaml_config

def check_global_static_files(static_files, filename):
    if not isinstance(static_files, list):
        error(f"Unsupported global static files format, file: {filename}")

    valid_types = ['dir', 'file']
    for item in static_files:
        if not isinstance(item, dict):
            error(f"Each static file item must be a dictionary, file: {filename}, line: {line(item)}")

        if 'type' not in item or item['type'] not in valid_types:
            error(f"Invalid or missing 'type' in static file item, file: {filename}, line: {line(item)}")

        if 'path' not in item or not isinstance(item['path'], str):
            error(f"Missing or invalid 'path' in static file item, file: {filename}, line: {line(item)}")

        if 'name' not in item or not isinstance(item['name'], str):
            error(f"Missing or invalid 'name' in static file item, file: {filename}, line: {line(item)}")

    return True

def get_file_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def process_global_static_files(ctx):
    client = ctx['client']
    configs_path = ctx['configs_path']
    location = ctx.get('location', None)

    if not location:
        location = "global_static_files"

    configs = read_yaml_config(configs_path, location)
    if configs is None:
        return

    info("Checking if global static files are valid")
    for filename, static_files in configs.items():
        check_global_static_files(static_files, filename)

    info("Processing global static files")

    # Get all existing files from server
    server_files = {}
    paths_to_check = [""]
    while paths_to_check:
        current_path = paths_to_check.pop(0)
        files = client.get_all_static_files(path=current_path)
        for file in files:
            server_files[file['path']] = file
            if file['type'] == 'dir':
                paths_to_check.append(file['path'])

    for filename, static_files in configs.items():
        for item in static_files:
            path = os.path.dirname(item['path'])

            if item['type'] == 'dir':
                if item['path'] not in server_files:
                    try:
                        info(f"Creating directory: {item['path']}")
                        client.create_static_file_directory(item['name'], path=path, label=item.get('label', None))
                    except Exception as e:
                        error(f"Failed to create directory: {item['path']}", e)
            elif item['type'] == 'file':
                file_path = os.path.join(configs_path, location, "files", item['path'])
                if not os.path.exists(file_path):
                    error(f"File not found: {file_path}")
                    continue

                local_md5 = get_file_md5(file_path)

                if item['path'] in server_files:
                    server_file = server_files[item['path']]
                    server_content = client.get_static_file_content(server_file['id'])
                    server_md5 = hashlib.md5(server_content).hexdigest()

                    if local_md5 != server_md5:
                        try:
                            info(f"Updating file: {item['path']}")
                            with open(file_path, 'rb') as file:
                                content = file.read()
                            client.set_static_file(server_file['id'], item['name'], content, path=path, label=item.get('label', None))
                        except Exception as e:
                            error(f"Failed to update file: {item['path']}", e)
                else:
                    try:
                        info(f"Uploading new file: {item['path']}")
                        with open(file_path, 'rb') as file:
                            content = file.read()
                        client.upload_static_file(item['name'], content, path=path, label=item.get('label', None))
                    except Exception as e:
                        error(f"Failed to upload file: {item['path']}", e)

    # since this is a global configuration,
    # we will not perform deletion operations in order to maintain compatibility with multiple local configurations.
    # # Check for files to delete
    # local_paths = set(item['path'] for filename, static_files in configs.items() for item in static_files)
    # for server_path in server_files:
    #     if server_path not in local_paths:
    #         try:
    #             info(f"Deleting file: {server_path}")
    #             client.del_static_file(server_files[server_path]['id'])
    #         except Exception as e:
    #             error(f"Failed to delete file: {server_path}", e)

def cleanup_global_static_files(ctx):
    pass
    # since this is a global configuration,
    # we will not perform deletion operations in order to maintain compatibility with multiple local configurations.
    # client = ctx['client']

    # try:
    #     info("Removing all global static files")
    #     files = client.get_all_static_files()
    #     for file in files:
    #         file_id = file['id']
    #         client.del_static_file(file_id)
    # except Exception as e:
    #     error("Failed to remove all global static files", e)

def export_global_static_files(ctx):
    client = ctx['client']
    configs_path = ctx['export_to_path']
    location = ctx.get('location', None)

    if not location:
        location = "global_static_files"

    next_paths = [ "" ]

    formatted_static_dirs = []
    formatted_static_files = []

    while next_paths:
        path = next_paths.pop(0)
    # for path in next_paths:
        static_files = client.get_all_static_files(path=path)
        if not static_files:
            break

        for item in static_files:
            formatted_item = {
                'type': item['type'],
                'path': item['path'],
                'name': item['name']
            }

            work_dir=os.path.join(configs_path, location, "files")

            try:
                if item['type'] == 'file':
                    formatted_static_files.append(formatted_item)
                    content = client.get_static_file_content(item['id'])
                    file_path = os.path.join(work_dir, item['path'])
                    os.makedirs(os.path.dirname(file_path), exist_ok=True)
                    with open(file_path, 'wb') as file:
                        file.write(content)
                else:
                    formatted_static_dirs.append(formatted_item)
                    file_path = os.path.join(work_dir, item['path'])
                    os.makedirs(file_path, exist_ok=True)
                    next_paths.append(item['path'])

                info(f"Exported file content to: {file_path}")
            except Exception as e:
                error(f"Failed to export file content: {item['path']}", e)

    export_path = os.path.join(configs_path, location)

    formatted_static_files = formatted_static_dirs + formatted_static_files

    if formatted_static_files:
        try:
            write_yaml_config(export_path, "global_static_files.yaml", formatted_static_files)
            info("Global static files configuration exported successfully to global_static_files/global_static_files.yaml")
        except Exception as e:
            error("Failed to export global static files configuration", e)
    else:
        info("No global static files found")
