#!/usr/bin/env python3

"""Local configuration for the client"""

import os
import yaml
import functools

def config_file_name():
    return os.path.join(os.getenv('HOME'), '.timed-client')


@functools.lru_cache()
def load():
    if not os.path.exists(config_file_name()):
        return {}

    with open(config_file_name()) as fh:
        config = yaml.load(fh)

    if not isinstance(config, dict):
        # Config broken or empty, reset
        return {}
    return config


def store(config):
    with open(config_file_name(), 'w') as fh:
        yaml.dump(config, fh)


def get(key):
    data = load()
    return data.get(key)

def put(key, value):
    data = load()
    data[key] = value
    store(data)
