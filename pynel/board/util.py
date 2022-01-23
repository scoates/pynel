import json


def get_dir(file_dunder):
    return "/".join(file_dunder.split("/", 2)[:-1])


def get_path(file_dunder, filename):
    return "/".join([get_dir(file_dunder), filename])


def get_config(filename=None):
    if filename is None:
        filename = get_path(__file__, "config.json")
    with open(filename) as f:
        return json.load(f)
