# -*- coding: utf-8 -*-

import os
import re
import json
import yaml
import fnmatch
from functools import reduce
import blitzdb
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.sql import select

def get_project_path(path=None):
    if not path:
        path = os.getcwd()
    while path != "/":
        config_path = os.path.join(path, '.checkmate')
        if os.path.exists(config_path) and os.path.isdir(config_path):
            return path
        path = os.path.dirname(path)
    return None


def get_project_config(path):
    with open(os.path.join(path, ".checkmate/config.json"), "r") as config_file:
        return json.loads(config_file.read())


def save_project_config(path, config):
    with open(os.path.join(path, ".checkmate/config.json"), "w") as config_file:
        config_file.write(json.dumps(config))


def get_files_list(path, with_sha=False):
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path):
        files.extend([(os.path.join(dirpath, f))[len(path):]
                     for f in filenames])
    return files


def apply_filter(filename, patterns):
    return reduce(lambda x, y: x or y, [True if re.search(pattern, filename, re.UNICODE)
                                        else False for pattern in patterns], False)


def filter_filenames_by_analyzers(filenames, analyzers, language_patterns):
    filtered_filenames = []
    for filename in filenames:
        for analyzer_params in analyzers:
            if not analyzer_params['language'] in language_patterns:
                continue
            language_pattern = language_patterns[analyzer_params['language']]
            if not 'patterns' in language_pattern \
                    or not apply_filter(filename, language_pattern['patterns']):
                continue
            filtered_filenames.append(filename)
            break
    return filtered_filenames


def filter_filenames_by_checkignore(file_paths, checkignore_patterns):

    filtered_file_paths = []

    for file_path in file_paths:
        excluded = False
        always_included = False
        for pattern in checkignore_patterns:
            if pattern.startswith("!"):
                if fnmatch.fnmatch(file_path, pattern[1:]):
                    always_included = True
                    break
            if fnmatch.fnmatch(file_path, pattern):
                excluded = True
        if not excluded or always_included:
            filtered_file_paths.append(file_path)
    return filtered_file_paths


def parse_checkmate_settings(content):
    """
    Basically a simple .yml parser that returns a simple Python dict to be used later on.
    """
    return yaml.safe_load(content)


def parse_checkignore(content):
    lines = [l for l in [s.strip() for s in content.split("\n")]
             if l and not l[0] == '#']
    return lines


def get_project_and_backend(path, settings, echo=False, initialize_db=True):
    project_path = get_project_path(path)
    project_config = get_project_config(project_path)
    backend = get_backend(project_path, project_config, settings, echo=echo, initialize_db=initialize_db)
    project = get_project(project_path, project_config, settings, backend)
    return project, backend


def get_backend(project_path, project_config, settings, echo=False, initialize_db=True):
    """
    Returns the appropriate backend instance based on the project configuration and settings.

    :param project_path: The path to the project directory.
    :param project_config: The configuration dictionary for the project.
    :param settings: Additional settings.
    :return: An instance of SQLBackend configured with the chosen backend.
    """
    # Get the backend configuration from the project configuration
    backend_config = project_config.get('backend', {})
    backend_type = backend_config.get('driver', 'sqlite') 
    connection_string = backend_config.get('connection_string', None)

    if backend_type == "sql":
      if not connection_string:
        raise ValueError("Connection string is required for the 'sql' backend.")
      engine = create_engine(connection_string)
      backend = SQLBackend(engine=engine)

    # Default to a generic Backend if not handled
    else:
      backend = Backend()  # Assuming this is a default generic backend class

    if initialize_db:
        backend.create_tables()

    return backend


def get_project(project_path, project_config, settings, backend):
    project_class = project_config.get('project_class', 'Project')
    ProjectClass = settings.models[project_class]

    try:
        project = backend.query(ProjectClass).filter_by(pk=project_config['project_id']).first()
    except ProjectClass.DoesNotExist:
        project = ProjectClass(pk=project_config['project_id'])
        backend.add(project)
        # we retrieve the project from the DB, so that all the hooks get executed properly.
        project = backend.query(ProjectClass).filter_by(pk=project_config['project_id']).first()

    project.path = project_path

    backend.add(project)

    return project

