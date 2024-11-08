from collections import namedtuple
import os
import json

DataSettings = namedtuple(
    'DataSettings', 'experiment_type, modi, data_folder, output_names, \
      include_input_features, exclude_input_features, mode, metric, normalization, batchsize, \
      output_folder, num_total, delimiter, augmented_features, verbose')


def handle_relative_paths(content, data_folder):
    data_folder = os.path.normpath(data_folder)
    for path_name in ["data_folder", "output_folder"]:
        if path_name == "output_folder" and content.get(path_name, "") == "":
            content[path_name] = data_folder.replace(os.path.join("data"), os.path.join("outputs"))
        # Check if the path is already absolute
        if os.path.isabs(content[path_name]):
            continue  # Skip if absolute path
        # Construct a relative path using os.path.join
        rel_path = os.path.join(data_folder, content[path_name])
        abs_path = os.path.abspath(rel_path)
        # Ensure the path has a trailing separator if it’s a directory
        content[path_name] = os.path.join(abs_path, "")
    return content


def json_to_data_settings(content, data_folder: str = None):
    if isinstance(content, str):
        content = json.loads(content)
    if data_folder is not None:
        content = handle_relative_paths(content, data_folder)
    data_settings = DataSettings(**content)
    return data_settings


def load_data_settings_file(data_settings_path, data_folder):
    data_settings = None
    with open(data_settings_path, "r") as file:
        content = json.load(file)
        data_settings = json_to_data_settings(content, data_folder)
        print(f"loaded data settings from file: {data_settings_path}")
    return data_settings


def save_data_settings_file(data_settings, data_settings_path):
    with open(data_settings_path, "w") as file:
        data_settings_dict = data_settings._asdict()
        json.dump(data_settings_dict, file, indent=4)
