#!/bin/bash

fork=true
evg_notify_file=~/.evg-notify
evg_notify_path=~/dev/evg-notify

# if we are not submitting a patch, just pass through args to evergreen
if [[ "$1" != "patch-file" && "$1" != "patch" ]]; then
    evergreen $@
    exit $?
fi

# log the output of the evergreen command to a file
# without changing the user's interaction with the cmd
script -q "$evg_notify_file" evergreen $@

# get the patch ID from evergreen output
patch_id=$(grep ID "$evg_notify_file" | awk '{print $3;}')

# remove the temporary file
rm "$evg_notify_file"

if [ "$fork" = "true" ]; then
    nohup python $evg_notify_path/src/main.py --patch $patch_id > /dev/null 2>&1 & disown
else
    python $evg_notify_path/src/main.py --patch $patch_id
fi
