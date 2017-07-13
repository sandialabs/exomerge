#!/bin/bash

# run style checker
bash style_check.sh
if [ $? -ne 0 ]; then
    echo "ERROR: Style check failed." >&2
    exit 1
fi

# set update message to arguments, or default
if [ $# -lt 1 ]; then
    message="Updates"
else
    message=$@
fi

git add -A && git commit -a -m "$message" && git push
