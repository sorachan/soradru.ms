#!/bin/bash

find images -name '*.meta.json' -exec rm {} \;
rm -rf galleries
mkdir galleries
for i in $(find images \( -name "*jpg" -o -name "*png" -o -name "*webp" -o -name "*mp4" -o -name "*mkv" -o -name "*avi" -o -name "*webm" -o -name "*lnk" \))
do
    fn=${i##*/}
    for j in $(find images-old -name "$fn")
    do
        path=${j%%/$fn}
        gall=${path##images-old/}
        if [ ! -f $i.meta.json ]
        then
            echo '{"galleries":[' > $i.meta.json
        fi
        if grep $gall $i.meta.json 2>/dev/null
        then
            echo "$gall already exists in $i.meta.json"
        else
            echo "adding $gall to $i.meta.json"
            echo "\"$gall\"," >> $i.meta.json
        fi
    done
    sed -e '$ s/.$//' -i .foo $i.meta.json
    rm -f $i.meta.json.foo
    echo ']}' >> $i.meta.json
done