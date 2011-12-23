'''
    logmon.config
    -------------

    Flask configuration.
'''


class Config(object):
    SITE_NAME = 'Logmon'
    SITE_DOMAIN = 'localhost'
    
    # indicates the file to watch
    LOG_FILE = '/var/log/nginx/access.log'
