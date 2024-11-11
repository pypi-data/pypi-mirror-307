import os
import io

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString

from .utils import error, warn, info, line

def read_yaml_file(file):
    yaml = YAML()
    with open(file, 'r') as f:
        config = yaml.load(f)

    return config

def read_yaml_config(configs_path, keyword=None):
    yaml = YAML()
    yaml_config = {}

    file_path = None
    directory_path = configs_path
    if keyword is not None:
        file_path = f"{configs_path}/{keyword}.yaml"
        directory_path = f"{configs_path}/{keyword}"

        if os.path.isfile(file_path) and os.path.isdir(directory_path):
            warn(f"the file and directory both exist; prioritize using the file: {file_path}")

    # check if file exists
    if file_path is not None and os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            config = yaml.load(f)

        yaml_config[f"{keyword}.yaml"] = config
        return yaml_config

    res = dict()
    # check if directory exists
    if os.path.isdir(directory_path):
        for filename in os.listdir(directory_path):
            if filename.endswith('.yaml'):
                full_path = os.path.join(directory_path, filename)
                with open(full_path, 'r') as f:
                    yaml_config[filename] = yaml.load(f)
        return yaml_config

    # not found
    return None

def read_lua_modules(configs_path, folder):
    folder = f"{configs_path}/{folder}"
    if not os.path.isdir(folder):
        # not found
        return None

    lua_files_content = {}
    for filename in os.listdir(folder):
        if filename.endswith('.lua'):
            file_key = os.path.splitext(filename)[0]
            file_path = os.path.join(folder, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                lua_files_content[file_key] = file.read()

    return lua_files_content


def write_yaml_config(configs_path, filename, config=None):
    yaml = YAML()
    yaml.default_flow_style = False
    yaml.indent(mapping=2, sequence=2, offset=0)

    if not os.path.exists(configs_path):
        os.makedirs(configs_path)

    file_path = os.path.join(configs_path, filename)

    with open(file_path, 'w') as f:
        yaml.dump(config, f)

    return file_path


from datetime import datetime

def prepare_export_path(partition_id, domain):
    current_path = os.getcwd()

    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

    dir_name = f"oredge-configs-{partition_id}-{domain}-{current_datetime}"

    full_path = os.path.join(current_path, dir_name)

    os.makedirs(full_path, exist_ok=True)

    return full_path

def format_yaml_content(content):
    return LiteralScalarString(content)

def add_before_comment(data, key, comment, indent=2):
    yaml = YAML()

    stream = io.StringIO()
    yaml.dump(data, stream)
    yaml_str = stream.getvalue()

    loaded_data = yaml.load(yaml_str)

    loaded_data.yaml_set_comment_before_after_key(key, before=comment, indent=indent)

    return loaded_data
