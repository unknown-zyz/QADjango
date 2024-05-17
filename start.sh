#!/bin/bash
python manage.py qcluster &
python manage.py runserver 0.0.0.0:8000
tail -f /dev/null