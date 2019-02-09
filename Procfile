web: gunicorn electricity.wsgi
worker: celery -A electricity worker -E -B -l debug
