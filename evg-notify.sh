#!/bin/bash

fork=true
evergreen=$
evg_notify_path=~/.evg-notify
evg_config_file=~/.evergreen.yml

# if we are not submitting a patch, just pass through args to evergreen
if [ "$1" != "patch-file" && "$1" != "patch" ]; then
    evergreen $@
    exit $?
fi

evergreen $@ awk
nohup python $evg_notify_path/src/main.py > /dev/null 2>&1 & disown


