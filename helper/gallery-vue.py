#!/usr/bin/python3

import sys
import os
import cv2
import json
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

usage = "usage: " + sys.argv[0] + " [gallery name (folder: images/name)]"

try:
    _, name = sys.argv
    folder = "images/" + name
    html = [
        '<div class="pswp-gallery" id="pswp-' + name + '">',
        '    <a v-for="(image, key) in imagesData"',
        '        :key="key"',
        '        :href="image.largeURL"',
        '        :data-pswp-width="image.width"',
        '        :data-pswp-height="image.height"',
        '        target="_blank"',
        '        rel="noreferrer"',
        '        :data-video="image.video">',
        '        <img :src="image.thumbnailURL"',
        '            :alt="image.alt"',
        '            :data-credit="image.credit"',
        '            :data-camera="image.camera"',
        '            :data-date="image.date"',
        '            :data-location="image.location"/>',
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
    for filename in sorted(os.listdir(folder), reverse=True):
        path = os.path.join(folder, filename)
        base, extension = os.path.splitext(filename)
        if filename == '.DS_Store' \
            or filename.endswith(".thumb.png") \
            or filename.endswith(".alt") \
            or filename.endswith(".camera") \
            or filename.endswith(".credit") \
            or filename.endswith(".date") \
            or filename.endswith(".loc") \
            or filename.endswith(".json"):
            continue
        print("processing " + filename)
        if extension in [".jpg", ".png", ".webp"]:
            image = cv2.imread(path)
            height, width, _ = image.shape
            alt=""
            credit = ""
            date = ""
            location = ""
            video = ""
            imagePIL = Image.open(path)
            exif = imagePIL.getexif()
            if os.path.isfile(path + ".json"):
                try:
                    obj = json.loads("".join(open(path + ".json").readlines()))
                    if type(obj) == dict and "instaloader" in obj.keys():
                        if obj["instaloader"].get("node_type") == "Post":
                            node = obj["node"]
                            alt += '<span class="insta-caption"><a href="https://instagram.com/p/' \
                                + node["shortcode"] + '"><span class="icon fab fa-instagram"></span></a> '
                            alt += node["edge_media_to_caption"]["edges"][0]["node"]["text"]
                            alt += '</span>'
                            time = datetime.fromtimestamp(node["taken_at_timestamp"])
                            date = "%d.%d.%d %d:%02d:%02d" % (
                                time.year, time.month, time.day,
                                time.hour, time.minute, time.second
                            )
                            user = node["owner"]["username"]
                            credit = (
                                '<a href="https://instagram.com/'
                                + user
                                + '"><span class="icon fab fa-instagram"></span> '
                                + user
                                + '</a>'
                            )
                            if type(node["location"]) == dict:
                                location = node["location"]["name"]
                except Exception as e:
                    print("parsing of JSON file " + path + ".json failed!")
                    print(e)
            if os.path.isfile(path + ".alt"):
                alt = "".join(open(path + ".alt").readlines()).strip()
            if os.path.isfile(path + ".credit"):
                credit = open(path + ".credit").readline().strip()
            if os.path.isfile(path + ".camera"):
                camera = open(path + ".camera").readline().strip()
            else:
                make = exif.get(list(TAGS.keys())[list(TAGS.values()).index("Make")], "")
                model = exif.get(list(TAGS.keys())[list(TAGS.values()).index("Model")], "")
                camera = " ".join([make, model]).strip()
            if not date:
                if os.path.isfile(path + ".date"):
                    date = open(path + ".date").readline().strip()
                else:
                    date = exif.get(list(TAGS.keys())[list(TAGS.values()).index("DateTime")], "")
                    if date:
                        day, time = date.split(" ")
                        day = ".".join([N.lstrip("0") for N in day.split(":")])
                        date = " ".join([day, time])
            if os.path.isfile(path + ".loc"):
                location = open(path + ".loc").readline().strip()
            thumbPath = path + ".thumb.png"
            if not os.path.isfile(path + ".thumb.png"):
                thumbHeight = 500
                thumbWidth = int(width * thumbHeight / height)
                thumb = cv2.resize(image, (thumbWidth, thumbHeight))
                cv2.imwrite(thumbPath, thumb)
            if os.path.isfile(os.path.join(folder, base) + ".mp4"):
                video = os.path.join(folder, base) + ".mp4"
            if os.path.isfile(os.path.join(folder, base) + ".mkv"):
                video = os.path.join(folder, base) + ".mkv"
            if os.path.isfile(os.path.join(folder, base) + ".webm"):
                os.path.join(folder, base) + ".webm"
            js += [
                "                {",
                "                    largeURL: " + json.dumps(path) + ",",
                "                    thumbnailURL: " + json.dumps(thumbPath) + ",",
                "                    width: " + str(width) + ",",
                "                    height: " + str(height) + ",",
                "                    alt: " + json.dumps(alt) + ",",
                "                    credit: " + json.dumps(credit) + ",",
                "                    camera: " + json.dumps(camera) + ",",
                "                    date: " + json.dumps(date) + ",",
                "                    location: " + json.dumps(location) + ",",
                "                    video: " + json.dumps(video),
                "                },"
            ]
        if extension in [".mp4", ".avi", ".mkv", ".webm"]:
            vid = cv2.VideoCapture(path)
            width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
            thumbPath = path + ".thumb.png"
            if not os.path.isfile(thumbPath) \
                and not os.path.isfile(os.path.join(folder, base) + ".jpg.thumb.png"):
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
        "            let dateHTML = '';",
        "            let locationHTML = '';",
        "            if (currSlideElement) {",
        "                captionHTML = currSlideElement.querySelector('img').getAttribute('alt');",
        "                creditHTML = currSlideElement.querySelector('img').getAttribute('data-credit');",
        "                cameraHTML = currSlideElement.querySelector('img').getAttribute('data-camera');",
        "                dateHTML = currSlideElement.querySelector('img').getAttribute('data-date');",
        "                locationHTML = currSlideElement.querySelector('img').getAttribute('data-location');",
        "            }",
        "            el.innerHTML = '';",
        "            if (captionHTML) {",
        """                el.innerHTML += '<div class="photo-caption">' + captionHTML;""",
        "            }",
        "            if (cameraHTML) {",
        """                el.innerHTML += '<div class="photo-camera">' + cameraHTML;""",
        "            }",
        "            if (creditHTML) {",
        """                el.innerHTML += '<div class="photo-credit">' + creditHTML;""",
        "            }",
        "            if (dateHTML) {",
        """                el.innerHTML += '<div class="photo-date">' + dateHTML;""",
        "            }",
        "            if (locationHTML) {",
        """                el.innerHTML += '<div class="photo-location">' + locationHTML;""",
        "            }",
        "        });}",
        "    });",
        "});",
        "lightbox_" + name + ".addFilter('itemData', (itemData, index) => {",
        "    const video = itemData.element.dataset.video;",
        "    if (video) {",
        "        itemData.video = video;",
        "    }",
        "    return itemData;",
        "});",
        "lightbox_" + name + ".on('contentLoad', (e) => {",
        "    const { content, isLazy } = e;",
        "    if (content.data.element.dataset.video) {",
        "        content.videoDiv = document.createElement('div');",
        "        content.videoDiv.classList.add('video-div');",
        "        content.videoDiv.classList.add('pswp__img');",
        "        const videoElement = document.createElement('video');",
        "        videoElement.src = content.data.element.dataset.video;",
        "        const overlay = document.createElement('div');",
        "        overlay.classList.add('video-overlay');",
        "        overlay.addEventListener('click', () => {",
        "            overlay.classList.add('playing');",
        "            videoElement.play();"
        "        });",
        "        videoElement.addEventListener('click', () => {",
        "            videoElement.pause();",
        "            overlay.classList.remove('playing');",
        "        });",
        "        const button = document.createElement('div');",
        "        button.classList.add('video-button');",
        "        button.innerHTML = '▶️';",
        "        overlay.appendChild(button);",
        "        content.videoDiv.appendChild(videoElement);",
        "        content.videoDiv.appendChild(overlay);",
        "        content.state = 'loading';",
        "        content.onLoaded();",
        "    }",
        "});",
        "lightbox_" + name + ".on('contentAppend', (e) => {",
        "    const { content } = e;",
        "    if (content.videoDiv && !content.videoDiv.parentNode) {",
        "        e.preventDefault();",
        "        content.slide.container.appendChild(content.videoDiv);",
        "    }",
        "});",
        "lightbox_" + name + ".init();"
    ]
    html += ['    ' + line for line in js]
    html += [
        '</script>'
    ]
    gallery = open("./galleries/" + name + ".html", "w")
    gallery.write("\n".join(html))
    gallery.flush()
    gallery.close()
except Exception as e:
    print("encountered an error")
    print(e)
    print(usage)