#!/bin/bash

cd safesight_django
python manage.py migrate &
python manage.py runserver 0.0.0.0:8000 &

cd ../safesight_api
uvicorn main:app --host 0.0.0.0 --port 8002
