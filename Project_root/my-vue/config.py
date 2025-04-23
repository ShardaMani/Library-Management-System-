from datetime import timedelta


class Config(object):
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    # Celery configurations for Redis
    broker="redis://localhost:6380/0",
    backend="redis://localhost:6380/1",
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
    timezone = 'Asia/Kolkata'

    # Cache configurations for Redis
    CACHE_TYPE = 'RedisCache'
    CACHE_DEFAULT_TIMEOUT = 200

    CACHE_REDIS_URL = 'redis://localhost:6380/2'
    REDIS_URL = "redis://localhost:6380"



