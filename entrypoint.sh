#!/bin/bash
service nginx start
cd /app
gunicorn -t 240 --bind unix:/app/gunicorn.sock main:app
