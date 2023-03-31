#!/usr/bin/python3

import sys
import os
import cv2
import json
from PIL import Image
from PIL.ExifTags import TAGS

usage = "usage: " + sys.argv[0] + "[gallery name (folder: images/name)] [indent level]"

try:
    _, name, indent = sys.argv
    folder = "images/" + name
    html = [
        '<div class="pswp-gallery" id="pswp-' + name + '">',
        '    <a v-for="(image, key) in imagesData"',
        '        :key="key"',
        '        :href="image.largeURL"',
        '        :data-pswp-width="image.width"',
        '        :data-pswp-height="image.height"',
        '        target="_blank"',
        '        rel="noreferrer">',
        '        <img :src="image.thumbnailURL"',
        '            :alt="image.alt"',
        '            :data-credit="image.credit"',
        '            :data-camera="image.camera"/>',
        '    </a>',
        '</div>',
        '<script type="module">'
    ]
    js = [
        'const { createApp } = Vue;',
        'createApp({',
        '    data() {',
        '        return {',
        '            imagesData: ['
    ]
    for filename in sorted(os.listdir(folder)):
        path = os.path.join(folder, filename)
        extension = os.path.splitext(filename)[-1]
        if filename.endswith(".thumb.png") \
            or filename.endswith(".alt") \
            or filename.endswith(".camera") \
            or filename.endswith(".credit"):
            continue
        print("processing " + filename)
        if extension in [".jpg", ".png", ".webp"]:
            image = cv2.imread(path)
            height, width, _ = image.shape
            alt=""
            credit = "own photography"
            if os.path.isfile(path + ".camera"):
                camera = open(path + ".camera").readline().strip()
            else:
                imagePIL = Image.open(path)
                exif = imagePIL.getexif()
                make = exif.get(list(TAGS.keys())[list(TAGS.values()).index("Make")], "")
                model = exif.get(list(TAGS.keys())[list(TAGS.values()).index("Model")], "")
                camera = " ".join([make, model]).strip()
            if os.path.isfile(path + ".alt"):
                alt = open(path + ".alt").readline().strip()
            if os.path.isfile(path + ".credit"):
                credit = open(path + ".credit").readline().strip()
            thumbPath = path + ".thumb.png"
            if not os.path.isfile(path + ".thumb.png"):
                thumbHeight = 500
                thumbWidth = int(width * thumbHeight / height)
                thumb = cv2.resize(image, (thumbWidth, thumbHeight))
                cv2.imwrite(thumbPath, thumb)
            js += [
                "                {",
                "                    largeURL: " + json.dumps(path) + ",",
                "                    thumbnailURL: " + json.dumps(thumbPath) + ",",
                "                    width: " + str(width) + ",",
                "                    height: " + str(height) + ",",
                "                    alt: " + json.dumps(alt) + ",",
                "                    credit: " + json.dumps(credit) + ",",
                "                    camera: " + json.dumps(camera),
                "                },"
            ]
        if extension in [".mp4", ".avi", ".mkv", ".webm"]:
            vid = cv2.VideoCapture(path)
            width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
            thumbPath = path + ".thumb.png"
            if not os.path.isfile(thumbPath):
                vid.set(cv2.CAP_PROP_POS_MSEC, 10000)
                _, thumb = vid.read()
                cv2.imwrite(thumbPath, thumb)
            vid.release()
            # TODO
        if extension == ".lnk":
            pass # TODO
    js += [
        '            ]',
        '        }',
        '    }',
        '}).mount("#pswp-' + name + '");',
        'import PhotoSwipeLightbox from "./photoswipe/dist/photoswipe-lightbox.esm.js";',
        'const lightbox_' + name + ' = new PhotoSwipeLightbox({',
        '    gallery: "#pswp-' + name + '",',
        '    children: "a",',
        '    pswpModule: () => import("./photoswipe/dist/photoswipe.esm.js")',
        '});',
        "lightbox_" + name + ".on('uiRegister', function() {",
        "    lightbox_" + name + ".pswp.ui.registerElement({",
        "        name: 'custom-caption',",
        "        isButton: false,",
        "        appendTo: 'root',",
        "        onInit: (el, pswp) => {",
        "        lightbox_" + name + ".pswp.on('change', () => {",
        "            const currSlideElement = lightbox_" + name + ".pswp.currSlide.data.element;",
        "            let captionHTML = '';",
        "            let creditHTML = '';",
        "            let cameraHTML = '';",
        "            if (currSlideElement) {",
        "                captionHTML = currSlideElement.querySelector('img').getAttribute('alt');",
        "                creditHTML = currSlideElement.querySelector('img').getAttribute('data-credit');",
        "                cameraHTML = currSlideElement.querySelector('img').getAttribute('data-camera');",
        "            }",
        "            el.innerHTML = captionHTML || '';",
        "            if (cameraHTML) {",
        """                el.innerHTML += '<div class="photo-camera">' + cameraHTML;""",
        "            }",
        "            if (creditHTML) {",
        """                el.innerHTML += '<div class="photo-credit">' + creditHTML;""",
        "            }",
        "        });}",
        "    });",
        "});",
        'lightbox_' + name + '.init();'
    ]
    html += ['    ' + line for line in js]
    html += [
        '</script>'
    ]
    pad = int(indent) * '    '
    html = [pad + line for line in html]
    gallery = open("./galleries/" + name + ".html", "w")
    gallery.write("\n".join(html))
    gallery.flush()
    gallery.close()
except Exception as e:
    print("encountered an error")
    print(e)
    print(usage)