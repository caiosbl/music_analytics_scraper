import os
from configparser import ConfigParser


def init_config_with_envs(config_file):
    config = ConfigParser()
    config.read(config_file)

    for section in config.sections():
        for key in config[section]:
            value = config[section][key]
            formatted_value = value.format(**os.environ)
            config[section][key] = formatted_value

    return config