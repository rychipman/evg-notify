#!/bin/bash

fork=false
evergreen=evergreen
evg_notify_file=~/.evg-notify
evg_notify_path=~/dev/evg-notify

# if we are not submitting a patch, just pass through args to evergreen
if [[ "$1" != "patch-file" && "$1" != "patch" ]]; then
    evergreen $@
    exit $?
fi

# log the output of the evergreen command to a file
# without changing the user's interaction with the cmd
script --version > /dev/null 2>&1
exit_code=$?
if [ "$exit_code" = "0" ]; then
    # Linux script
    cmd="$evergreen $@"
    script -q -c "$cmd" "$evg_notify_file"
    evg_exit_code=$?
else
    # BSD script
    script -q "$evg_notify_file" $evergreen $@
    evg_exit_code=$?
fi

if [ "$evg_exit_code" != "0" ]; then
    exit $evg_exit_code
fi

# get the patch ID from evergreen output
patch_id=$(grep ID "$evg_notify_file" | awk '{print $3}' | awk '{ sub(/\r/,""); print }')

# remove the temporary file
rm "$evg_notify_file"

if [ "$fork" = "true" ]; then
    nohup python $evg_notify_path/src/main.py --patch $patch_id > /dev/null 2>&1 & disown
else
    python $evg_notify_path/src/main.py --patch $patch_id
fi
