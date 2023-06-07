#!/usr/bin/env python3
import os
import yaml
from .macros import file_type_to_extension
from .pipeline import Pipeline


def load_config(cfg_path: str) -> dict:
    """load the yaml config file

    Args:
        cfg_path (str): path to the yaml config file

    Returns:
        dict: config dictionary
    """
    with open(cfg_path) as f:
        cfg: dict = yaml.safe_load(f)
    return cfg

def print_dict(d: dict, indent: int = 0) -> None:
    """print a dictionary with indentation, uses recursion to print nested dictionaries
    
    Args:
        d (dict): dictionary to be printed
        indent (int, optional): indentation level. Defaults to 0.

    Returns:
        None
    """
    for key, value in d.items():
        if isinstance(value, dict):
            print('  ' * indent + str(key) + ": ")
            print_dict(value, indent+1)
        else:
            print('  ' * indent + str(key) + ": " + str(value))

def verify_file(path: str, type: str) -> bool:
    """verify that the file/directory exists and is of the correct type

    Args:
        path (str): verified file/directory path
        type (str): verified file/directory type

    Returns:
        bool: True if the file/directory exists and is of the correct type
    """
    # verify the file/directory exists
    assert os.path.exists(path), f'file {path} does not exist'

    # verify the file type is supported
    assert type in file_type_to_extension.keys(), f'file type {type} is not supported'

    # verify the file type matches the extension or the path is a directory
    if type == "directory":
        assert os.path.isdir(path), f'{path} is not a directory'
    else:
        assert os.path.splitext(path)[-1] == file_type_to_extension[type], f'file {path} is not a {type} file'

    return True


def trace_config(cfg: dict) -> list:
    """trace the config file, print the pipelines, and initializes the pipeline threads

    Args:
        cfg (dict): config dictionary from load_config()

    Returns:
        list: list of pipeline threads 
    """
    pipelines = []
    # verify that the config file contains "pipelines"
    assert "pipelines" in cfg and cfg["pipelines"], "pipeline is not specified in config file"

    print('Loaded config:')
    print("pipelines: ", end="")
    print(cfg["pipelines"], end="\n\n")

    for pipeline_name in cfg["pipelines"]:
        # verify that the pipeline is specified in the config file
        assert pipeline_name in cfg, f'pipeline {pipeline_name} is not specified in config file'

        pipeline = cfg[pipeline_name]

        # make directories for output and verify type
        for index, output in pipeline["output"].items():
            # verify the file type is supported
            assert output["type"] in file_type_to_extension.keys(), f'pipeline {pipeline_name}\'s output {index}\'s file type {output["type"]} is not supported'

            # make parent directories if they don't exist
            output["directory"] = os.path.dirname(output["path"]) if (output["type"] == "directory") else os.path.dirname(output["path"])
            os.makedirs(output["directory"], exist_ok=True)

        # verify input
        assert verify_file(path = pipeline["input"]["path"], type = pipeline["input"]["type"]), f'pipeline {pipeline_name}\'s input file {pipeline["input"]["path"]} is not valid'

        print(pipeline_name + ":")
        print_dict(pipeline, indent=1)

        pipelines.append(Pipeline(pipeline_name, pipeline))

    return pipelines
