#!/usr/bin/python3

import sys
import os
import cv2

usage = "usage: " + sys.argv[0] + " [folder (should be images/*)] [gallery name] [indent level]"

try:
    _, folder, name, indent = sys.argv
    html = ['<div class="pswp-gallery" id="van">']
    for filename in sorted(os.listdir(folder)):
        path = os.path.join(folder, filename)
        extension = os.path.splitext(filename)[-1]
        if extension in [".jpg", ".png", ".webp"]:
            image = cv2.imread(path)
            width, height, _ = image.shape
            html += [
                '    <a href="' + path + '"',
                '        data-pswp-width="' + str(width) + '"',
                '        data-pswp-height="' + str(height) + '"',
                '        target="_blank">',
                '        <img src="' + path + '" alt= "" />'
                '    </a>'
            ]
        if extension in [".mp4", ".avi", ".mkv", ".webm"]:
            vid = cv2.VideoCapture(path)
            width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if extension == ".lnk":
            pass
except Exception as e:
    print("encountered an error")
    print(e)
    print(usage)