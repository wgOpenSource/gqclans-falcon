formatters = {
    'descriptive': {
        'format': '%(asctime)s\t%(levelname)-5.5s\t[%(name)s.%(funcName)s]:\t%(message)s',
        'datefmt': '%d/%b/%Y %H:%M:%S',
    },
    'generic': {
        'format': '[%(levelname)s]P:%(process)d T:%(thread)d %(asctime)s %(name)s.%(funcName)s: %(message)s',
        'datefmt': '%d/%b/%Y %H:%M:%S',
    },
    'simple': {
        'format': '[%(levelname)s|%(name)s] %(message)s',
        'datefmt': '%d/%b/%Y %H:%M:%S',
    }
}

handlers = {
    'console': {
        'class': 'logging.StreamHandler',
        '_stream': 'stdout',
        'formatter': 'generic',
    },
}

loggers = {
    '': {
        'level': 'INFO',
        'handlers': ['console'],
    },
}
