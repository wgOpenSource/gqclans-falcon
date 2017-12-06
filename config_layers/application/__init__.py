import os

from config_layers.application import (
    db,
    loggers,
)

__config_modules__ = (
    db,
    loggers,
)

project_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.path.pardir, os.path.pardir)
