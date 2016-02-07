#!/bin/bash
FILENAME=$(date +"%Y-%m-%d")

chmod go+w .
python manage.py models_info 2>> $FILENAME.dat
chmod 700 .
