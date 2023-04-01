#!/bin/bash

for path in images/*
do
    if [[ "${path##images/}" == "credits" ]]
    then
        continue
    fi
    if [ -d "$path" ]
    then
        find $path -type f -exec bash -c 'mv "$1" "`echo "$1" | tr "[:upper:]" "[:lower:]"`"' _ '{}' \; # force lower-case file names
        name="${path##images/}"
        ./helper/gallery-vue.py "$name"
    fi
done
