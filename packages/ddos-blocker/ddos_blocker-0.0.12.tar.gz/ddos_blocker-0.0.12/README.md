Documentation under development. 

At this point you can already use the library. 
In the config file settings.py add:

REDIS_HOST = 'host'
REDIS_PORT = 'port'
REDIS_DB = '0 - 16'
REDIS_TIMEOUT = 'if the user makes more than REDIS_MAX_REQUESTS requests during this time, he will be blocked' 
REDIS_MAX_REQUESTS = 'maximum number of requests'

Default settings:

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_TIMEOUT = 5 * 60
REDIS_MAX_REQUESTS = 100