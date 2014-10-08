#web: gunicorn activersity_datacenter.wsgi --log-file -
#web: python manage.py runserver 0.0.0.0:$PORT --noreload
web: uwsgi --http :$PORT --wsgi-file activersity_datacenter/wsgi.py