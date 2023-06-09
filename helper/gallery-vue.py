#!/usr/bin/python3

import sys
import os
import cv2
import json
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime
import requests
import re
import pyktok as pyk
from pytube import YouTube

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
        '        :data-video="image.video"',
        '        :data-extsrc="image.extsrc">',
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
            or filename == '.ds_store' \
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
                            alt = '<span class="insta-caption"><a href="https://instagram.com/p/' \
                                + node["shortcode"] \
                                + '"><span class="icon fab fa-instagram"></span></a> ' \
                                + node["edge_media_to_caption"]["edges"][0]["node"]["text"] \
                                + '</span>'
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
            if os.path.isfile(path + ".date"):
                date = open(path + ".date").readline().strip()
            elif not date:
                date = exif.get(list(TAGS.keys())[list(TAGS.values()).index("DateTime")], "")
                if date:
                    day, time = date.split(" ")
                    day = ".".join([N.lstrip("0") for N in day.split(":")])
                    date = " ".join([day, time])
            if os.path.isfile(path + ".loc"):
                location = open(path + ".loc").readline().strip()
            thumb_path = path + ".thumb.png"
            if not os.path.isfile(path + ".thumb.png"):
                thumbHeight = 500
                thumbWidth = int(width * thumbHeight / height)
                thumb = cv2.resize(image, (thumbWidth, thumbHeight))
                cv2.imwrite(thumb_path, thumb)
            if os.path.isfile(os.path.join(folder, base) + ".mp4"):
                video = os.path.join(folder, base) + ".mp4"
            if os.path.isfile(os.path.join(folder, base) + ".mkv"):
                video = os.path.join(folder, base) + ".mkv"
            if os.path.isfile(os.path.join(folder, base) + ".webm"):
                video = os.path.join(folder, base) + ".webm"
            js += [
                "                {",
                "                    largeURL: " + json.dumps(path) + ",",
                "                    thumbnailURL: " + json.dumps(thumb_path) + ",",
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
            if os.path.isfile(os.path.join(folder, base) + ".jpg"):
                continue
            vid = cv2.VideoCapture(path)
            width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
            thumb_path = path + ".thumb.png"
            if not os.path.isfile(thumb_path):
                vid.set(cv2.CAP_PROP_POS_MSEC, 1000)
                _, thumb = vid.read()
                cv2.imwrite(thumb_path, thumb)
            vid.release()
            alt=""
            credit = ""
            date = ""
            location = ""
            camera = ""
            video = path
            if os.path.isfile(path + ".alt"):
                alt = "".join(open(path + ".alt").readlines()).strip()
            if os.path.isfile(path + ".credit"):
                credit = open(path + ".credit").readline().strip()
            if os.path.isfile(path + ".camera"):
                camera = open(path + ".camera").readline().strip()
            if os.path.isfile(path + ".date"):
                date = open(path + ".date").readline().strip()
            if os.path.isfile(path + ".loc"):
                location = open(path + ".loc").readline().strip()
            js += [
                "                {",
                "                    largeURL: " + json.dumps(thumb_path) + ",",
                "                    thumbnailURL: " + json.dumps(thumb_path) + ",",
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
        if extension == ".lnk":
            link = "".join(open(path).readlines()).strip()
            alt=""
            camera=""
            credit = ""
            date = ""
            location = ""
            extsrc = ""
            thumb_path = ""
            if "youtube.com" in link or "youtu.be" in link:
                if "watch?v=" in link:
                    id = link.split("watch?v=")[-1]
                elif ".be/" in link:
                    id = link.split(".be/")[-1]
                extsrc = "https://www.youtube.com/embed/" + id
                thumb_path = "https://img.youtube.com/vi/" + id + "/0.jpg"
                thumb = None
                thumb = requests.get(thumb_path)
                with open("/tmp/thumb.png", "wb") as f:
                    f.write(thumb.content)
                image = cv2.imread("/tmp/thumb.png")
                height, width, _ = image.shape
                video = None
                while not video:
                    video = YouTube("https://youtu.be/" + id)
                alt = '<span class="insta-caption"><a href="https://youtu.be/' \
                    + id \
                    + '"><span class="icon fab fa-youtube"></span></a> ' \
                    + video.description \
                    + '</span>'
                time = video.publish_date
                date = "%d.%d.%d" % (time.year, time.month, time.day)
                credit = (
                    '<a href="'
                    + video.channel_url
                    + '"><span class="icon fab fa-youtube"></span> '
                    + video.author
                    + '</a>'
                )
                if os.path.isfile(path + ".alt"):
                    alt = "".join(open(path + ".alt").readlines()).strip()
                if os.path.isfile(path + ".credit"):
                    credit = open(path + ".credit").readline().strip()
                if os.path.isfile(path + ".camera"):
                    camera = open(path + ".camera").readline().strip()
                if os.path.isfile(path + ".date"):
                    date = open(path + ".date").readline().strip()
                if os.path.isfile(path + ".loc"):
                    location = open(path + ".loc").readline().strip()
                js += [
                    "                {",
                    "                    largeURL: " + json.dumps(thumb_path) + ",",
                    "                    thumbnailURL: " + json.dumps(thumb_path) + ",",
                    "                    width: " + str(width) + ",",
                    "                    height: " + str(height) + ",",
                    "                    alt: " + json.dumps(alt) + ",",
                    "                    credit: " + json.dumps(credit) + ",",
                    "                    camera: " + json.dumps(camera) + ",",
                    "                    date: " + json.dumps(date) + ",",
                    "                    location: " + json.dumps(location) + ",",
                    "                    extsrc: " + json.dumps(extsrc),
                    "                },"
                ]
            if "vimeo.com" in link:
                id = link.split("/")[-1]
                extsrc = "https://player.vimeo.com/video/" + id
                thumb_url = "https://vimeo.com/api/v2/video/" + id + ".json"
                thumb_req = requests.get(thumb_url)
                thumb_data = thumb_req.json()
                thumb_path = thumb_data[0]["thumbnail_large"].replace("http:", "https:")
                thumb = requests.get(thumb_path)
                with open("/tmp/thumb.png", "wb") as f:
                    f.write(thumb.content)
                image = cv2.imread("/tmp/thumb.png")
                height, width, _ = image.shape
                if os.path.isfile(path + ".alt"):
                    alt = "".join(open(path + ".alt").readlines()).strip()
                if os.path.isfile(path + ".credit"):
                    credit = open(path + ".credit").readline().strip()
                if os.path.isfile(path + ".camera"):
                    camera = open(path + ".camera").readline().strip()
                if os.path.isfile(path + ".date"):
                    date = open(path + ".date").readline().strip()
                if os.path.isfile(path + ".loc"):
                    location = open(path + ".loc").readline().strip()
                js += [
                    "                {",
                    "                    largeURL: " + json.dumps(thumb_path) + ",",
                    "                    thumbnailURL: " + json.dumps(thumb_path) + ",",
                    "                    width: " + str(width) + ",",
                    "                    height: " + str(height) + ",",
                    "                    alt: " + json.dumps(alt) + ",",
                    "                    credit: " + json.dumps(credit) + ",",
                    "                    camera: " + json.dumps(camera) + ",",
                    "                    date: " + json.dumps(date) + ",",
                    "                    location: " + json.dumps(location) + ",",
                    "                    extsrc: " + json.dumps(extsrc),
                    "                },"
                ]
            if "tiktok.com" in link:
                # TODO, TikTok embed are just too much of a PITA rn
                tok = pyk.get_tiktok_json(link)
                with open("/tmp/tokjson", "w") as f:
                    f.write(json.dumps(tok, indent=4))
                try:
                    item_dict = tok["ItemModule"]
                    id = list(item_dict.keys())[0]
                    item = item_dict[id]
                    alt = '<span class="insta-caption"><a href="' \
                        + tok["SEOState"]["metaParams"]["canonicalHref"] \
                        + '"><span class="icon fab fa-tiktok"></span></a> ' \
                        + item["desc"] + '</span>'
                    time = datetime.fromtimestamp(int(item["createTime"]))
                    date = "%d.%d.%d %d:%02d:%02d" % (
                        time.year, time.month, time.day,
                        time.hour, time.minute, time.second
                    )
                    user = item["author"]
                    credit = (
                        '<a href="https://tiktok.com/@'
                        + user
                        + '"><span class="icon fab fa-tiktok"></span> '
                        + user
                        + '</a>'
                    )
                    if type(item["poi"]) == dict:
                        location = item["poi"]["name"]
                except Exception as e:
                    print("parsing of JSON file " + path + ".json failed!")
                    print(e)
            if "vk.com" in link:
                pass # TODO
            if "facebook.com" in link:
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
        """                el.innerHTML += '<div class="photo-caption">' + captionHTML + '</div>';""",
        r"""                el.innerHTML += '<img src="?" onerror="alert(\'foo\'); for (const element of document.querySelectorAll(\'.photo-caption\')) { if (element.scrollHeight > element.clientHeight || element.scrollWidth > element.clientWidth) element.classList.add(\'overflown\'; }" />';""",
        "            }",
        "            if (cameraHTML) {",
        """                el.innerHTML += '<div class="photo-camera">' + cameraHTML + '</div>';""",
        "            }",
        "            if (creditHTML) {",
        """                el.innerHTML += '<div class="photo-credit">' + creditHTML + '</div>';""",
        "            }",
        "            if (dateHTML) {",
        """                el.innerHTML += '<div class="photo-date">' + dateHTML + '</div>';""",
        "            }",
        "            if (locationHTML) {",
        """                el.innerHTML += '<div class="photo-location">' + locationHTML + '</div>';""",
        "            }",
        "        });}",
        "    });",
        "});",
        "lightbox_" + name + ".addFilter('itemData', (itemData, index) => {",
        "    const video = itemData.element.dataset.video;",
        "    const extsrc = itemData.element.dataset.extsrc;",
        "    if (video) {",
        "        itemData.video = video;",
        "    }",
        "    if (extsrc) {",
        "        itemData.extsrc = extsrc;",
        "    }",
        "    return itemData;",
        "});",
        "lightbox_" + name + ".on('contentLoad', (e) => {",
        "    const { content, isLazy } = e;",
        "    if (content.data.element.dataset.video) {",
        "        content.videoDiv = document.createElement('div');",
        "        content.videoDiv.classList.add('video-div');",
        "        content.videoDiv.classList.add('pswp__img');",
        "        const wrapper = document.createElement('div');",
        "        wrapper.classList.add('video-wrapper');",
        "        const videoElement = document.createElement('video');",
        "        videoElement.src = content.data.element.dataset.video;",
        "        const overlay = document.createElement('div');",
        "        overlay.classList.add('video-overlay');",
        "        overlay.addEventListener('click', () => {",
        "            overlay.classList.add('playing');",
        "            videoElement.play();",
        "        });",
        "        videoElement.addEventListener('click', () => {",
        "            videoElement.pause();",
        "            overlay.classList.remove('playing');",
        "        });",
        "        videoElement.addEventListener('ended', () => {",
        "            videoElement.pause();",
        "            overlay.classList.remove('playing');",
        "        });",
        "        const button = document.createElement('div');",
        "        button.classList.add('video-button');",
        "        button.innerHTML = '▶️';",
        "        overlay.appendChild(button);",
        "        wrapper.appendChild(videoElement);",
        "        wrapper.appendChild(overlay);",
        "        content.videoDiv.appendChild(wrapper);",
        "        content.state = 'loading';",
        "        content.onLoaded();",
        "    }",
        "    if (content.data.element.dataset.extsrc) {",
        "        content.iframeDiv = document.createElement('div');",
        "        content.iframeDiv.classList.add('iframe-div');",
        "        content.iframeDiv.classList.add('pswp__img');",
        "        const wrapper = document.createElement('div');",
        "        wrapper.classList.add('iframe-wrapper');",
        "        wrapper.style.width = content.data.element.dataset.pswpWidth;",
        "        wrapper.style.height = content.data.element.dataset.pswpHeight;",
        "        const iframeElement = document.createElement('iframe');",
        "        iframeElement.src = content.data.element.dataset.extsrc;",
        "        iframeElement.setAttribute('allowFullScreen', '');",
        "        iframeElement.style.width = content.data.element.dataset.pswpWidth;",
        "        iframeElement.style.height = content.data.element.dataset.pswpHeight;",
        "        const overlay = document.createElement('div');",
        "        overlay.classList.add('iframe-overlay');",
        "        overlay.addEventListener('click', () => {",
        "            overlay.classList.add('playing');",
        "            wrapper.appendChild(iframeElement);",
        "        });",
        "        const button = document.createElement('div');",
        "        button.classList.add('iframe-button');",
        "        button.innerHTML = '⚠️';",
        "        const warning = document.createElement('div');",
        "        warning.classList.add('iframe-warning');",
        "        warning.innerHTML = '<p>warning!</p>'",
        "            + '<p>you are about to load an external iframe from <em>'",
        "            + new URL(iframeElement.src).hostname",
        "            + '</em>, by doing so you agree to their cookie and privacy policies!</p>';",
        "        overlay.appendChild(warning);"
        "        overlay.appendChild(button);",
        "        wrapper.appendChild(overlay);",
        "        content.iframeDiv.appendChild(wrapper);",
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
        "    if (content.iframeDiv && !content.iframeDiv.parentNode) {",
        "        e.preventDefault();",
        "        content.slide.container.appendChild(content.iframeDiv);",
        "    }",
        "});",
        "lightbox_" + name + ".on('contentRemove', (e) => {",
        "    const { content } = e;",
        "    if (content.videoDiv && content.videoDiv.parentNode) {",
        "        e.preventDefault();",
        "        content.videoDiv.remove();",
        "    }",
        "    if (content.iframeDiv && content.iframeDiv.parentNode) {",
        "        e.preventDefault();",
        "        content.iframeDiv.remove();",
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
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    print(usage)