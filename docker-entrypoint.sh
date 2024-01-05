#!/bin/bash
set -e

echo ">>> Log Level taken from the env file: '$LOG_LEVEL'"
echo ">>> Input file taken from env file: '$CONFIG_FILE'"

if [ "$LOG_LEVEL" = "" ]; then
    echo ">>> Running without '--log' argument"
    python -u server.py --f=$CONFIG_FILE
else
echo ">>> Running with '--log' argument"
    python -u server.py --f=$CONFIG_FILE --log=$LOG_LEVEL
fi