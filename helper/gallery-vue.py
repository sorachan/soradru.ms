#!/usr/bin/python3

import sys
import os
import cv2
import json

usage = "usage: " + sys.argv[0] + " [folder (should be images/*)] [gallery name] [indent level]"

try:
    _, folder, name, indent = sys.argv
    html = [
        '<div class="pswp-gallery" id="' + name + '">',
        '    <a v-for="(image, key) in imagesData"',
        '        :key="key"',
        '        :href="image.largeURL"',
        '        :data-pswp-width="image.width"',
        '        :data-pswp-height="image.height"',
        '        target="_blank"',
        '        rel="noreferrer">',
        '        <img :src="image.thumbnailURL" :alt="image.alt" :data-credit="image.credit"/>',
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
        if extension in [".jpg", ".png", ".webp"] and not filename.endswith(".thumb.png"):
            image = cv2.imread(path)
            height, width, _ = image.shape
            alt=""
            credit = "own photography"
            if os.path.isfile(path + ".alt"):
                alt = open(path + ".alt").readline().strip()
            if os.path.isfile(path + ".credit"):
                credit = open(path + ".credit").readline().strip()
            js += [
                "                {",
                "                    largeURL: " + json.dumps(path) + ",",
                "                    thumbnailURL: " + json.dumps(path) + ",", # TODO
                "                    width: " + str(width) + ",",
                "                    height: " + str(height) + ",",
                "                    alt: " + json.dumps(alt) + ",",
                "                    credit: " + json.dumps(credit),
                "                },"
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
            # TODO
        if extension == ".lnk":
            pass # TODO
    js += [
        '            ]',
        '        }',
        '    }',
        '}).mount("#' + name + '");',
        'import PhotoSwipeLightbox from "./photoswipe/dist/photoswipe-lightbox.esm.js";',
        'const lightbox_' + name + ' = new PhotoSwipeLightbox({',
        '    gallery: "#' + name + '",',
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
        "            if (currSlideElement) {",
        "                captionHTML = currSlideElement.querySelector('img').getAttribute('alt');",
        "                creditHTML = currSlideElement.querySelector('img').getAttribute('data-credit');",
        "            }",
        "            el.innerHTML = captionHTML || '';",
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