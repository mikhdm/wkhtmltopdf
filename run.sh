#!/bin/bash

PORT=${PORT:-8000}

docker run --rm -it -p $PORT:8000 --name wkhtmltopdf wkhtmltopdf:latest 
