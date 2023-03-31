#!/bin/bash

name=$1

for img in images/$name/*.jpg
do
    echo "🌄 $img"
    pxl $img
    echo "💬 caption?"
    read caption
    echo $caption > $img.alt
    echo "📸 photography credit?"
    read credit
    rm -f $img.credit
    if [ ! -z $credit ]
    then
        touch images/credits/$credit.credit
        ln -v images/credits/$credit.credit $img.credit
    fi
done