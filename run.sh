#!/bin/bash
docker-compose exec server python manage.py recreate_db
docker-compose exec server python manage.py seed_db

open http://0.0.0.0:5001/apidocs/

