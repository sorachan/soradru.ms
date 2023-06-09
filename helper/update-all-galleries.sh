#!/bin/bash

rm -rf galleries
mkdir galleries
for path in $(find images -type d -mindepth 1)
do
    if [[ "${path##images/}" == "resources" ]]
    then
        continue
    fi
    if [ -d "$path" ]
    then
        echo "[ $path ]"
        find $path -type f -exec bash -c 'mv "$1" "`echo "$1" | tr "[:upper:]" "[:lower:]"`"' _ '{}' \; # force lower-case file names
        name="${path##images/}"
        ./helper/gallery-json.py "$name"
    fi
done
