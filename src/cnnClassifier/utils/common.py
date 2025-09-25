import os
from box.exceptions import BoxValueError
from yaml import YAMLError
import yaml
from cnnClassifier import logger
import json
from pathlib import Path
from typing import Any
from ensure import ensure_annotations
from box import ConfigBox
import joblib
import base64


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads a yaml file and returns a ConfigBox object

    Args:
        path_to_yaml (Path): Path to the yaml file

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: ConfigBox object
    """
    try:
        with open(path_to_yaml, "r") as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError as e:
        raise BoxValueError(f"Error while converting yaml to configbox: {e}")
    except YAMLError as e:
        raise YAMLError(f"Error while reading yaml file: {e}")
    

@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """Create list of directories

    Args:
        path_to_directories (list): List of directories to be created
        ignore_log (bool, optional): ignore logging if multiple directories are to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """Saves a dictionary to a json file

    Args:
        path (Path): Path to the json file
        data (dict): data to be saved
    """
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"json file saved at: {path}")

