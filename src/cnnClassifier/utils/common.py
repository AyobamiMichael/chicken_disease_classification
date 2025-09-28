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


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """load json files data
    Args:
        path (Path): path to the json file
    
    Returns:
        ConfigBox: data as class attributes instead of dictionary

    """
    with open(path, "r") as f:
        content = json.load(f)
    logger.info(f"json file: {path} loaded successfully")
    return ConfigBox(content)

@ensure_annotations
def save_bin(data: Any, path: Path):
    """save any data type as binary file

    Args:
        data (Any): data to be saved
        path (Path): path to the binary file
    """
    joblib.dump(value=data, filename=path)
    logger.info(f"binary file saved at: {path}")

@ensure_annotations
def load_bin(path: Path) -> Any:
    """load binary data

    Args:
        path (Path): path to the binary file

    Returns:
        Any: data stored in the binary file
    """
    data = joblib.load(filename=path)
    logger.info(f"binary file: {path} loaded successfully")
    return data

@ensure_annotations
def get_size(path: Path) -> str:
    """get size in KB

    Args:
        path (Path): path to the file

    Returns:
        str: size in KB
    """
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"

def decodeImage(imagestring, filName):
    imgdata = base64.b64decode(imagestring)
    with open(filName, 'wb') as f:
        f.write(imgdata)
        f.close()
    logger.info(f"Image saved at: {filName}")

def encodeImageIntoBase64(croppedImagePath):
    with open(croppedImagePath, "rb") as f:
        my_string = base64.b64encode(f.read())
        logger.info(f"Image encoded from: {croppedImagePath}")
        return my_string

