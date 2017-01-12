import logging
LOGGING = {
    'version' : 1,
    'disable_existing_loggers' : True,
    'formatters' : {
        'verbose': {
            'format' : '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple' : {
            'format' : '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'console': {
            'level' : 'DEBUG',
            'class' : 'logging.StreamHandler',
            'formatter' : 'simple',
        },
        'file': {
            'level' : 'DEBUG',
            'class' : 'logging.FileHandler',
            'filename' : '../logs/debug.log',
            'formatter' : 'simple',
        },
        'mail': {
            'level' : 'CRITICAL',
            'class' : 'logging.handlers.SMTPHandler',
            'formatter' : 'verbose',
            'mailhost' : 'smtps.kuleuven.be',
            'fromaddr' : 'auguste.colle@kuleuven.be',
            'toaddrs' : ['auguste.colle@kuleuven.be'],
            'subject' : 'BMS warning',
            'credentials' : ('u0094673', ''),
            'secure' : (),
        },
    },
    'loggers': {
        'app': {
            'handlers': ['file', 'console', 'mail'],
            'level' : 'DEBUG',
            'propagate' : True,
        },
        'logging2db': {
            'handlers': ['file', 'console', 'mail'],
            'level' : 'DEBUG',
            'propagate' : True,
        },
        'test': {
            'handlers': ['file', 'console', 'mail'],
            'level' : 'DEBUG',
            'propagate' : True,
        },
    },
}


