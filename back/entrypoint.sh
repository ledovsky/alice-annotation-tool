cd drf_backend
python manage.py migrate
python manage.py collectstatic --no-input
# gunicorn drf_backend.wsgi -b 0.0.0.0:8000 --worker-class=gevent --worker-connections=10 --workers=2
gunicorn drf_backend.wsgi -b 0.0.0.0:8000 --workers=2 --timeout 300