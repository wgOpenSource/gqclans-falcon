import os

PARENT_CONFIGURATION_LAYER = 'application'
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
DB_ADDR = os.environ.get('DB_ADDR')

class db:
    master = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_ADDR}:5432/{POSTGRES_DB}'


class loggers:
    handlers = {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'generic',
        },
    }

    loggers = {
        '': {
            'level': 'DEBUG',
            'handlers': ['console', ],
        },
    }


class nose:
    log_capturing = False
    stdout_capturing = False
