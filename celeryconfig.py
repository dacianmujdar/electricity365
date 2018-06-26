#celeryconfig.py

try:
	from local_celeryconfig import *
except ImportError:
	BROKER_URL = 'amqp://ohyqqudn:xagxV0lNAGzaDtO3VGOgpqmFyU8lbwxZ@wolverine.rmq.cloudamqp.com/ohyqqudn'
	BROKER_POOL_LIMIT = 1
	BROKER_CONNECTION_TIMEOUT = 10
	CELERYD_CONCURRENCY = 4
	CELERY_RESULT_BACKEND = 'amqp://ohyqqudn:xagxV0lNAGzaDtO3VGOgpqmFyU8lbwxZ@wolverine.rmq.cloudamqp.com/ohyqqudn'

	CELERY_TASK_SERIALIZER = 'json'
	CELERY_RESULT_SERIALIZER = 'json'
	CELERY_ACCEPT_CONTENT=['json']
	CELERY_TIMEZONE = 'Canada/Eastern'
	CELERY_ENABLE_UTC = True