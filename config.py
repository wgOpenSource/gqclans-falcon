import logging.config as logging_config
import os
import sys

from common.config import Options


def set_config(layer_name):
    # pylint: disable = global-statement
    global config

    environment_variable = 'APP_CONFIG'
    layer_name = os.getenv(environment_variable, layer_name)

    project_path = os.path.dirname(os.path.abspath(__file__))
    config_layers_path = os.path.join(project_path, 'config_layers')
    config = Options.from_filesystem(os.path.join(config_layers_path, layer_name))

    # override DB settings from env, if any
    config.db.master = os.getenv('DB_CONNECTION', config.db.master)

    # logging
    setup_loggers(config, loggers_configuration_attr='loggers')

    return config


def setup_loggers(config, loggers_configuration_attr):
    for data in config.loggers.handlers.values():
        if '_filename' in data:
            data['filename'] = os.path.join(config.loggers.logs_directory_path, data.pop('_filename'))
        if '_stream' in data:
            data['stream'] = getattr(sys, data.pop('_stream'))

    loggers_configuration = getattr(config, loggers_configuration_attr)
    logging_config.dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'loggers': loggers_configuration.loggers,
        'handlers': loggers_configuration.handlers,
        'formatters': config.loggers.formatters,
    })


config = set_config('infrastructure')
