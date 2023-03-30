#!/usr/bin/python3

import sys
import os
import cv2

usage = "usage: " + sys.argv[0] + " [folder (should be images/*)] [gallery name] [indent level]"

try:
    _, folder, name, indent = sys.argv
    js = [
        "import PhotoSwipeLightbox from './photoswipe/dist/photoswipe-lightbox.esm.js';",
        "const options = {",
        "    dataSource: ["
    ]
    html = [
        '<div class="pswp-gallery" id="' + name + '">'
    ]
    for filename in sorted(os.listdir(folder)):
        path = os.path.join(folder, filename)
        extension = os.path.splitext(filename)[-1]
        if extension in [".jpg", ".png", ".webp"] and not filename.endswith(".thumb.png"):
            image = cv2.imread(path)
            height, width, _ = image.shape
            js += [
                "        {",
                "            src: '" + path +"',",
                "            width: " + str(width) + ",",
                "            height: " + str(height) + ",",
                "            alt: ''",
                "        },"
            ]
        if extension in [".mp4", ".avi", ".mkv", ".webm"]:
            vid = cv2.VideoCapture(path)
            width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
            thumbpath = path + ".thumb.png"
            if not os.path.isfile(thumbpath):
                vid.set(cv2.CAP_PROP_POS_MSEC, 10000)
                _, thumb = vid.read()
                cv2.imwrite(thumbpath, thumb)
            vid.release()
            js += [
                "        {",
                r'''            html: '<div class="pswp-video-div">\n' ''',
                '''                + '    <video width="'''
                    + str(width)
                    + '" height="'
                    + str(height)
                    + r'''" controls>\n' ''',
                '''                + '        <source src="'''
                    + path
                    + '''" type="video/'''
                    + extension[1:]
                    + r'''">\n' ''',
                r"                + '    </video>\n'",
                "                + '</div>'",
                "        },"
            ]
        if extension == ".lnk":
            pass
    js += [
        "    ],",
        "    showHideAnimationType: 'none',",
        "    pswpModule: () => import('./photoswipe/dist/photoswipe.esm.js'),",
        "};",
        "const lightbox = new PhotoSwipeLightbox(options);",
        "lightbox.init();",
        "document.querySelector('#pswp-"
            + name
            + "').onclick = () => {",
        "    lightbox.loadAndOpen(0);",
        "};"
    ]
except Exception as e:
    print("encountered an error")
    print(e)
    print(usage)