#!/bin/bash

clear
echo "Initializing webserver"
python -m SimpleHTTPServer > /dev/null 2>&1 &
echo "Webserver initialized"

echo "Initializing measurements"
cd ./python/
./app.py > /dev/null 2>&1 &
echo "Measurements initialized"

ps aux | grep python

