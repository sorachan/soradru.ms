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
import pathlib

no_credit = True
no_credit = True
no_credit = True

usage = "usage: " + sys.argv[0] + " [image folder name]"

def traceback():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)

try:
    _, name = sys.argv
    folder = "images/" + name
    for filename in sorted(os.listdir(folder), reverse=True):
        path = os.path.join(folder, filename)
        base, extension = os.path.splitext(filename)
        if filename == '.DS_Store' \
            or filename == '.ds_store' \
            or filename.endswith(".thumb.png") \
            or filename.endswith(".json"):
            continue
        print("processing " + filename)
        meta = {}
        if extension in [".jpg", ".png", ".webp"]:
            image = cv2.imread(path)
            meta["height"], meta["width"], _ = image.shape
            imagePIL = Image.open(path)
            exif = imagePIL.getexif()
            # try to read camera make / model and date / time from EXIF metadata
            make = exif.get(list(TAGS.keys())[list(TAGS.values()).index("Make")], "")
            model = exif.get(list(TAGS.keys())[list(TAGS.values()).index("Model")], "")
            if make or model:
                meta["camera"] = {}
                if make:
                    meta["camera"]["make"] = make
                if model:
                    meta["camera"]["model"] = model
            exifDate = exif.get(list(TAGS.keys())[list(TAGS.values()).index("DateTime")], "")
            if exifDate:
                meta["date"] = {}
                meta["date"]["timeStamp"] = datetime.strptime(exifDate, "%Y:%m:%d %H:%M:%S").timestamp()
            # process instaloader JSON
            json_path = os.path.join(folder, base) + ".json"
            if os.path.isfile(json_path):
                try:
                    obj = json.loads("".join(open(json_path).readlines()))
                    if type(obj) == dict and "instaloader" in obj.keys():
                        if obj["instaloader"].get("node_type") == "Post":
                            node = obj["node"]
                            insta_caption = ""
                            if len(node["edge_media_to_caption"]["edges"]):
                                insta_caption = node["edge_media_to_caption"]["edges"][0]["node"]["text"]
                            meta["alt"] = '<span class="insta-caption"><a href="https://instagram.com/p/' \
                                + node["shortcode"] \
                                + '"><span class="icon fab fa-instagram"></span></a> ' \
                                + insta_caption \
                                + '</span>'
                            meta["date"] = {}
                            meta["date"]["timeStamp"] = node["taken_at_timestamp"]
                            if not no_credit:
                                meta["photoCredit"] = {}
                                meta["photoCredit"]["external"] = {}
                                meta["photoCredit"]["external"]["name"] = node["owner"]["username"]
                                meta["photoCredit"]["external"]["url"] = "https://instagram.com/" \
                                    + node["owner"]["username"] + '</a>'
                            if type(node["location"]) == dict:
                                location = node["location"]["name"]
                except Exception as e:
                    print("parsing of JSON file " + json_path + " failed!")
                    print(e)
                    traceback()
            # add video file to JSON
            if os.path.isfile(os.path.join(folder, base) + ".mp4"):
                meta["video"] = os.path.join(folder, base) + ".mp4"
            if os.path.isfile(os.path.join(folder, base) + ".mkv"):
                meta["video"] = os.path.join(folder, base) + ".mkv"
            if os.path.isfile(os.path.join(folder, base) + ".webm"):
                meta["video"] = os.path.join(folder, base) + ".webm"
            # generate thumbs
            thumb_path = path + ".thumb.png"
            if not os.path.isfile(path + ".thumb.png"):
                thumbHeight = 500
                thumbWidth = int(meta["width"] * thumbHeight / meta["height"])
                thumb = cv2.resize(image, (thumbWidth, thumbHeight))
                cv2.imwrite(thumb_path, thumb)
            meta["thumb"] = True
        elif extension in [".mp4", ".avi", ".mkv", ".webm"]:
            if os.path.isfile(os.path.join(folder, base) + ".jpg"):
                continue
            vid = cv2.VideoCapture(path)
            meta["width"] = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
            meta["height"] = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
            meta["video"] = path
            thumb_path = path + ".thumb.png"
            if not os.path.isfile(thumb_path):
                vid.set(cv2.CAP_PROP_POS_MSEC, 1000)
                _, thumb = vid.read()
                cv2.imwrite(thumb_path, thumb)
            vid.release()
            meta["thumb"] = True
        elif extension == ".lnk":
            link = "".join(open(path).readlines()).strip()
            if "youtube.com" in link or "youtu.be" in link:
                if "watch?v=" in link:
                    id = link.split("watch?v=")[-1]
                elif ".be/" in link:
                    id = link.split(".be/")[-1]
                meta["extsrc"] = "https://www.youtube.com/embed/" + id
                thumb_path = "https://img.youtube.com/vi/" + id + "/0.jpg"
                thumb = requests.get(thumb_path)
                with open(path + ".thumb.png", "wb") as f:
                    f.write(thumb.content)
                meta["thumb"] = True
                image = cv2.imread(path + ".thumb.png")
                height, width, _ = image.shape
                video = None
                while not video:
                    video = YouTube("https://youtu.be/" + id)
                meta["alt"] = '<span class="insta-caption"><a href="https://youtu.be/' \
                    + id \
                    + '"><span class="icon fab fa-youtube"></span></a> ' \
                    + video.description if video.description else '' \
                    + '</span>'
                time = video.publish_date
                meta["date"] = {}
                meta["date"]["timeString"] = "%d.%d.%d" % (time.year, time.month, time.day)
                if not no_credit:
                    meta["photoCredit"] = {}
                    meta["photoCredit"]["external"] = {}
                    meta["photoCredit"]["external"]["name"] = video.author
                    meta["photoCredit"]["external"]["url"] = video.channel_url
            if "vimeo.com" in link:
                id = link.split("/")[-1]
                meta["extsrc"] = "https://player.vimeo.com/video/" + id
                thumb_url = "https://vimeo.com/api/v2/video/" + id + ".json"
                thumb_req = requests.get(thumb_url)
                thumb_data = thumb_req.json()
                thumb_path = thumb_data[0]["thumbnail_large"].replace("http:", "https:")
                thumb = requests.get(thumb_path)
                with open(path + ".thumb.png", "wb") as f:
                    f.write(thumb.content)
                meta["thumb"] = True
                image = cv2.imread(path + ".thumb.png")
                height, width, _ = image.shape
            if "tiktok.com" in link: # TODO, TikTok embed are just too much of a PITA rn
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
                    traceback()
                continue
            if "vk.com" in link:
                continue # TODO
            if "facebook.com" in link:
                continue # TODO
        else:
            continue
        # process metadata JSON
        if os.path.isfile(path + ".meta.json"):
            try:
                metaJson = json.loads("".join(open(path + ".meta.json").readlines()), strict=False)
                if type(metaJson) == dict:
                    meta.update(metaJson)
            except Exception as e:
                print("parsing of JSON file " + path + ".meta.json failed!")
                print(e)
                traceback()
        # write metadata JSON
        with open(path + ".meta.json", "w") as f:
            f.write(json.dumps(meta, indent=4))
        # add to galleries
        if meta.get("galleries"):
            for gallery_name in meta["galleries"]:
                if os.path.isfile("galleries/" + gallery_name):
                    with open("galleries/" + gallery_name) as f:
                        if path + "\n" in f.readlines():
                            continue
                with open("galleries/" + gallery_name, "a") as f:
                    f.write(path + "\n")
        # TODO: tag friends
except Exception as e:
    print("encountered an error")
    print(e)
    traceback()
    print(usage)