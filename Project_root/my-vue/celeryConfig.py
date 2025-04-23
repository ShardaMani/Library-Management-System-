

CELERY_BROKER_URL = 'redis://localhost:6380/0'
RESULT_BACKEND = 'redis://localhost:6380/1'
timezone = "Asia/Kolkata"
broker_connection_retry_on_startup = True