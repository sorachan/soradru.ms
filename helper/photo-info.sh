#!/bin/bash

name=$1

for img in images/$name/*.jpg
do
    echo -e "[ 🌄 $img ($(./helper/get-exif.py "$img" Make) $(./helper/get-exif.py "$img" Model)) ]\n"
    pxl "$img"
    echo -e "[ 💬 caption? ]\n"
    if [ -f "$img".alt ]
    then
        echo -e "current caption:\n"
        cat "$img".alt
        echo
    fi
    if [ -f "$img".json ]
    then
        if python3 -c "import json; json.loads(''.join(open('$img.json').readlines()))['instaloader']" >/dev/null 2>&1
        then
            echo "instaloader json detected."
            if python3 -c "import json; json.loads(''.join(open('$img.json').readlines()))['node']['edge_media_to_caption']['edges'][0]['node']['text']" >/dev/null 2>&1
            then
                echo -e "Instagram caption:\n"
                python3 -c "import json; print(json.loads(''.join(open('$img.json').readlines()))['node']['edge_media_to_caption']['edges'][0]['node']['text'])"
                echo
                echo "setting the caption property will override the Instagram caption."
                echo "do you want to copy the Instagram caption span to the caption property first? (y/n)"
                read copyinsta
                echo
                if [[ $copyinsta == "y" ]]
                then
                    echo -n '<span class="insta-caption"><span class="icon fab fa-instagram"></span> ' > "$img".alt
                    python3 -c "import json; open('$img.alt', 'a').write(json.loads(''.join(open('$img.json').readlines()))['node']['edge_media_to_caption']['edges'][0]['node']['text'])"
                    echo '</span>' >> "$img".alt
                    echo -e "\nupdated caption:\n"
                    cat "$img".alt
                fi
            else
                echo "could not parse Instagram caption."
            fi
        fi
    fi
    if [ -f "$img".alt ]
    then
        echo "mode? ([l]eft append, [r]ight append, [o]pen in vi, (over)[w]rite, [-] remove, [] nothing (default))"
        read mode
        if [[ $mode == "-" ]]
        then
            rm "$img".alt
        fi
        if [[ $mode == "l" ]]
        then
            copy=$(mktemp)
            if cp "$img".alt $copy
            then
                tmp=$(mktemp)
                echo -e "\nenter text to prepend followed by ctrl+d:\n"
                cat > $tmp
                cat $tmp $copy > "$img".alt
                echo
                echo
            else
                echo "saving caption to temp file failed!"
            fi
        fi
        if [[ $mode == "r" ]]
        then
            echo -e "\nenter text to append followed by ctrl+d:\n"
            cat >> "$img".alt
            echo
            echo
        fi
        if [[ $mode == "o" ]]
        then
            vi "$img".alt
            echo
        fi
        if [[ $mode == "w" ]]
        then
            echo -e "\nenter new text followed by ctrl+d:\n"
            cat > "$img".alt
            echo
            echo
        fi
    else
        echo "add caption? (y/n)"
        read addcaption
        if [[ $addcaption == "y" ]]
        then
            echo -e "\nenter text followed by ctrl+d:\n"
            cat > "$img".alt
            echo
            echo
        fi
    fi
    echo -e "[ 📍 location? (can be left blank, "-" to delete) ]\n"
    if [ -f "$img".loc ]
    then
        echo "[ current location ]"
        cat "$img".loc
        echo
    fi
    read loc
    if [[ $loc == "-" ]]
    then
        rm -f "$img".loc
    else
        if [ ! -z $loc ]
        then
            echo $loc > "$img".loc
            echo
        fi
    fi
    echo -e "[ 🤳 photography credit? (can be left blank, "-" to delete) ]\n"
    if [ -f "$img".credit ]
    then
        echo "[ current credit ]"
        cat "$img".credit
        echo
    fi
    read credit
    if [[ $credit == "-" ]]
    then
        rm -f "$img".credit
    else
        if [ ! -z $credit ]
        then
            touch images/credits/$credit.credit
            echo
            ln -v images/credits/$credit.credit "$img".credit
        fi
    fi
done