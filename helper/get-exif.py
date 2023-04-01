#!/usr/bin/python3

import sys
from PIL import Image
from PIL.ExifTags import TAGS

usage = sys.argv[0] + " [image file] (optional: [desired property])"

try:
    path = sys.argv[1]
    img = Image.open(path)
    exifRaw = img.getexif()
    exifNamed = {TAGS[k]: v for k, v in dict(exifRaw).items()}
    if len(sys.argv) > 2:
        prop = sys.argv[2]
        print(exifNamed.get(prop, ""))
    else:
        print("\n".join([k + ": " + str(v) for k, v in dict(exifNamed).items()]))
except Exception as e:
    print("something went wrong!")
    print(e)
    print(usage)