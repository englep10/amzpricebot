from datetime import timedelta

BROKER_URL = 'amqp://guest@localhost//'
CELERY_RESULT_BACKEND = 'redis'

CELERY_TIMEZONE = 'UTC'

CELERYBEAT_SCHEDULE = {
    'everymin': {
      'task': 'myapp.test_beater',
      'schedule': timedelta(seconds=60),
    },
}
