#!/usr/bin/python3

import json
import os

# change to root of https://soradru.ms
if os.getcwd().endswith("helper"):
    os.chdir("..")

# collect .json files except for template.json
friend_jsons = [
    f for f in os.listdir("friends/")
    if f.endswith(".json") and not f == "template.json"
]
friends = []
for friend_json in friend_jsons:
    with open(os.path.join("friends", friend_json), "r") as friend_file:
        friend = json.loads("\n".join([
            line.replace("\\\\", "\\") 
            for line in friend_file.readlines()
        ]))
        friends += [friend]

# sort friends alphabetically
friends.sort(key=lambda friend: friend["general"]["name"])

# create ID to name dictionary for family relations
id_to_friend = {
    friend["general"]["id"]: friend["general"]["name"] for friend in friends
}

# sort friends by initials
friends_by_initials = {}
for friend in friends:
    initial = friend["general"]["name"][0]
    if initial not in friends_by_initials:
        friends_by_initials[initial] = [friend]
    else:
        friends_by_initials[initial] += [friend]

# compute offset for flag emojis
flag_offset = ord('🇦') - ord('A')

# build HTML code for https://soradru.ms/friends/friendbook.html include
html = []
for initial in friends_by_initials:
    html += [
        "<h2>",
        initial,
        "</h2>"
    ]
    for friend in friends_by_initials[initial]:
        if friend["css"]:
            html += [
                "<link rel=\"stylesheet\" href=\"" + "friends/"
                 + friend["general"]["id"] + ".css\">"
            ]
        html += [
            "<details id=\"" + friend["general"]["id"] + "\">",
            "<summary>",
            friend["general"]["name"]
        ]
        if friend["general"].get("died"):
            html += [
                "(†)"
            ]
        html += [
            "</summary>",
            "<div class=\"friendbook\">"
        ]
        if friend["general"].get("profilePic"):
            profile_pic = friend["general"]["profilePic"]
            html += [
                "<figure class=\"profile-pic\">",
                "<img src=\"" + profile_pic["url"] + "\">",
            ]
            if profile_pic.get("caption"):
                html += [
                    "<figcaption class=\"profile-pic-caption\">",
                    profile_pic["caption"],
                    "</figcaption>"
                ]
            if profile_pic.get("photoCredit"):
                credit = profile_pic["photoCredit"]
                html += [
                    "<figcaption class=\"profile-pic-credit\">",
                    "<strong>credit:</strong>"
                ]
                if credit.get("friendId"):
                    html += [
                        "<a href=\"#" + credit["friendId"] + "\">",
                        id_to_friend.get(credit["friendId"], ""),
                        "</a>"
                    ]
                elif credit.get("external"):
                    html += [
                        "<a href=\"" + credit["external"].get("url", "")+ "\">",
                        credit["external"].get("name", ""),
                        "</a>"
                    ]
                html += [
                    "</figcaption>"
                ]
            html += [
                "</figure>"
            ]
        if friend["general"].get("nicknames"):
            html += [
                "<div class=\"nicknames\">",
                "<strong>nicknames:</strong>",
                "<ul>"
            ]
            for nickname in friend["general"]["nicknames"]:
                html += [
                    "<li>",
                    nickname,
                    "</li>"
                ]
            html += [
                "</ul>",
                "</div>"
            ]
        if friend["general"].get("born"):
            born = friend["general"]["born"]
            html += [
                "<div class=\"born\">",
                "<strong>born:</strong>"
            ]
            if born.get("birthDate"):
                html += [
                    ".".join([str(i) for i in born["birthDate"]])
                ]
            elif born.get("birthYear"):
                html += [
                    born["birthYear"]
                ]
            elif born.get("birthApprox"):
                html += [
                    "approx. " + born["birthApprox"]
                ]
            if born.get("place"):
                html += [
                    "in"
                ]
                place = born["place"]
                place_str = ""
                if place.get("city"):
                    place_str += place["city"]
                if place.get("state"):
                    if place_str:
                        place_str += ", " + place["state"]
                    else:
                        place_str = place["state"]
                if place.get("country"):
                    if place_str:
                        place_str += " ("
                        place_str += "".join([
                            chr(ord(c) + flag_offset) for c in place["country"]
                        ])
                        place_str += ")"
                    else:
                        place_str = "".join([
                            chr(ord(c) + flag_offset) for c in place["country"]
                        ])
                html += [
                    place_str
                ]
            html += [
                "</div>"
            ]
        if friend["general"].get("died"):
            died = friend["general"]["died"]
            html += [
                "<div class=\"died\">",
                "<strong>died:</strong>"
            ]
            if died.get("deathDate"):
                html += [
                    ".".join([str(i) for i in died["deathDate"]])
                ]
            elif died.get("deathYear"):
                html += [
                    died["deathYear"]
                ]
            elif died.get("deathApprox"):
                html += [
                    "approx. " + friend["general"]["died"]["deathApprox"]
                ]
            if died.get("place"):
                html += [
                    "in"
                ]
                place = died["place"]
                place_str = ""
                if place.get("city"):
                    place_str += place["city"]
                if place.get("state"):
                    if place_str:
                        place_str += ", " + place["state"]
                    else:
                        place_str = place["state"]
                if place.get("country"):
                    if place_str:
                        place_str += " ("
                        place_str += "".join([
                            chr(ord(c) + flag_offset) for c in place["country"]
                        ])
                        place_str += ")"
                    else:
                        place_str = "".join([
                            chr(ord(c) + flag_offset) for c in place["country"]
                        ])
                html += [
                    place_str
                ]
                if died.get("cause"):
                    html += [
                        "<br><strong>cause:</strong> "
                        + died["cause"]
                    ]
                if died.get("suicide"):
                    if died["suicide"]:
                        html += [
                            " (suicide)"
                        ]
                if died.get("murdered"):
                    if died["murdered"]:
                        if died.get("murderedBy"):
                            html += [
                                "(murdered by",
                                died["murderedBy"] + ")"
                            ]
                        else:
                            html += [
                                "(murdered)"
                            ]
            html += [
                "</div>"
            ]
        if friend["general"].get("family"):
            family = friend["general"]["family"]
            html += [
                "<div class=\"family\">",
                "<strong>family:</strong>",
                "<ul>"
            ]
            for member in family:
                html += [
                    "<li>" + member["relation"] + ":",
                    "<a href=\"#" + member["id"] + "\">",
                    id_to_friend.get(member["id"], ""),
                    "</a>",
                    "</li>"
                ]
            html += [
                "</ul>",
                "</div>"
            ]
        phone_data = {
            "landline": "icon fas fa-phone",
            "mobile": "icon fas fa-mobile",
            "fax": "icon fas fa-fax"
        }
        if friend.get("phone"):
            phone_list = friend["phone"]
            html +=[
                "<div class=\"phone\">",
                "<strong>phone:</strong>",
                "<ul>"
            ]
            for number in phone_list:
                html += [
                    "<li>",
                    "<a href=\"tel:" + number["number"] + "\">"
                        + "<i class=\"" + phone_data.get(number["type"], "")
                        + "\"></i> " + number["number"] + "</a>",
                ]
                if number.get("whatsapp") \
                    or number.get("signal") \
                    or number.get("telegram"):
                    messenger = []
                    if number.get("whatsapp"):
                        messenger += ["WhatsApp"]
                    if number.get("signal"):
                        messenger += ["Signal"]
                    if number.get("telegram"):
                        messenger += ["Telegram"]
                    html += ["(" + ", ".join(messenger) + ")"]
                html += [
                    "</li>"
                ]
            html += [
                "</ul>",
                "</div>"
            ]
        socials_data = {
            "discord": [
                "https://discordapp.com/users/{}",
                "<i class=\"icon fab fa-discord\"></i> Discord"
            ],
            "facebook": [
                "https://facebook.com/{}",
                "<i class=\"icon fab fa-facebook\"></i> Facebook"
            ],
            "github": [
                "https://github.com/{}",
                "<i class=\"icon fab fa-github\"></i> GitHub"
            ],
            "instagram": [
                "https://instagram.com/{}",
                "<i class=\"icon fab fa-instagram\"></i> Instagram"
            ],
            "kik": [
                "kik://users/{}/profile",
                "Kik"
            ],
            "linkedin": [
                "https://www.linkedin.com/in/{}",
                "<i class=\"icon fab fa-linkedin\"></i> LinkedIn"
            ],
            "snapchat": [
                "https://snapchat.com/add/{}",
                "<i class=\"icon fab fa-snapchat\"></i> Snapchat"
            ],
            "tiktok": [
                "https://tiktok.com/@{}",
                "<i class=\"icon fab fa-tiktok\"></i> TikTok"
            ],
            "tumblr": [
                "https://{}.tumblr.com",
                "<i class=\"icon fab fa-tumblr\"></i> Tumblr"
            ],
            "twitch": [
                "https://twitch.tv/{}",
                "<i class=\"icon fab fa-twitch\"></i> Twitch"
            ],
            "vk": [
                "https://vk.com/{}",
                "<i class=\"icon fab fa-vk\"></i> VK"
            ],
            "youtube": [
                "https://youtube.com/{}",
                # note: older YT accs follow the URI scheme
                #     https://youtube.com/steenvoortl
                # while newer YT accs follow the URI scheme
                #     https://youtube.com/@sora_drums
                # please add @ in JSON if necessary
                "<i class=\"icon fab fa-youtube\"></i> YouTube"
            ],
            "xing": [
                "https://www.xing.com/profile/{}",
                "<i class=\"icon fab fa-xing\"></i> Xing"
            ],
            "web": [
                "{}",
                "Website"
            ]
        }
        if friend.get("socials"):
            socials = friend["socials"]
            html += [
                "<div class=\"socials\">",
                "<strong>socials:</strong>",
                "<ul>"
            ]
            for social in socials:
                if not social.startswith("comment"):
                    if socials[social].startswith("https://"):
                        url = socials[social]
                    else:
                        url = socials_data[social][0].format(socials[social])
                    html += [
                        "<li>",
                        "<a href=\"" + url + "\">",
                        socials_data[social][1],
                        "</a>",
                        "</li>"
                    ]
            html +=[
                "</ul>",
                "</div>"
            ]
        gamer_tags_data = {
            "ingress": "Ingress: {}",
            "pokemongo": "Pokémon Go: {}",
            "psn": "PlayStation Network: {}",
            "steam": "Steam: {}",
            "xbox": "Xbox: {}"
        }
        if friend.get("gamerTags"):
            gamer_tags = friend["gamerTags"]
            html += [
                "<div class=\"gamer-tags\">",
                "<strong>gamer tags:</strong>",
                "<ul>"
            ]
            for tag in gamer_tags:
                html += [
                    "<li>",
                    gamer_tags_data[tag].format(gamer_tags[tag]),
                    "</li>"
                ]
            html +=[
                "</ul>",
                "</div>"
            ]
        contact_data = {
            "telegram": [
                "https://t.me/{}",
                "<i class=\"icon fab fa-telegram\"></i> Telegram"
            ],
            "icq": [
                "https://icq.im/{}",
                "ICQ"
            ],
            "email": [
                "mailto:{}",
                "<i class=\"icon fas fa-envelope\"></i> E-Mail"
            ],
            "matrix": [
                "https://matrix.to/#/{}",
                "Matrix"
            ]
        }
        if friend.get("contact"):
            html += [
                "<div class=\"contact\">",
                "<strong>contact:</strong>",
                "<ul>"
            ]
            contact = friend["contact"]
            for platform in contact:
               url = contact_data[platform][0].format(contact[platform])
               html += [
                   "<li>",
                   "<a href=\"" + url + "\">",
                   contact_data[platform][1],
                   "</a>",
                   "</li>"
               ]
            html += [
                "</ul>",
                "</div>"
            ]
        if friend.get("food"):
            html += [
                "<div class=\"food\">"
            ]
            if friend["food"].get("dishes"):
                html += [
                    "<strong>favourite dishes:</strong>",
                    "<ul>"
                ]
                for dish in friend["food"]["dishes"]:
                    html += [
                        "<li>",
                        dish,
                        "</li>"
                    ]
                html += [
                    "</ul>"
                ]
            if friend["food"].get("restaurants"):
                html += [
                    "<strong>favourite restaurants:</strong>",
                    "<ul>"
                ]
                for restaurant in friend["food"]["restaurants"]:
                    html += [
                        "<li>",
                        restaurant,
                        "</li>"
                    ]
                html += [
                    "</ul>"
                ]
            html += [
                "</div>"
            ]
        if friend.get("drinks"):
            html += [
                "<div class=\"drinks\">"
            ]
            if friend["drinks"].get("beverages"):
                html += [
                    "<strong>favourite beverages:</strong>",
                    "<ul>"
                ]
                for beverage in friend["drinks"]["beverages"]:
                    html += [
                        "<li>",
                        beverage,
                        "</li>"
                    ]
                html += [
                    "</ul>"
                ]
            if friend["drinks"].get("bars"):
                html += [
                    "<strong>favourite bars:</strong>",
                    "<ul>"
                ]
                for bar in friend["drinks"]["bars"]:
                    html += [
                        "<li>",
                        bar,
                        "</li>"
                    ]
                html += [
                    "</ul>"
                ]
            html += [
                "</div>"
            ]
        if friend.get("drugs"):
            html += [
                "<div class=\"drugs\">",
                "<strong>favourite drugs:</strong>",
                "<ul>"
            ]
            for drug in friend["drugs"]:
                html += [
                    "<li>",
                    drug,
                    "</li>"
                ]
            html += [
                "</ul>",
                "</div>"
            ]
        if friend.get("animals"):
            html += [
                "<div class=\"animal\">",
                "<strong>favourite animals:</strong>",
                "<ul>"
            ]
            for animal in friend["animals"]:
                html += [
                    "<li>",
                    animal,
                    "</li>"
                ]
            html += [
                "</ul>",
                "</div>"
            ]
        if friend.get("music"):
            if friend["music"].get("genres"):
                html += [
                    "<div class=\"genres\">",
                    "<strong>favourite genres:</strong>",
                    "<ul>"
                ]
                for genre in friend["music"]["genres"]:
                    html += [
                        "<li>",
                        genre,
                        "</li>"
                    ]
                html += [
                    "</ul>",
                    "</div>"
                ]
            if friend["music"].get("artists"):
                html += [
                    "<div class=\"artists\">",
                    "<strong>favourite artists:</strong>"
                    "<ul>"
                ]
                for artist in friend["music"]["artists"]:
                    html += [
                        "<li>",
                        "<a href=\"" + artist["url"] + "\">",
                        artist["name"],
                        "</a>",
                        "</li>"
                    ]
                html += [
                    "</ul>",
                    "</div>"
                ]
            if friend["music"].get("songs"):
                html += [
                    "<div class=\"songs\">",
                    "<strong>favourite songs:</strong>",
                    "<ul>"
                ]
                for song in friend["music"]["songs"]:
                    html += [
                        "<li>",
                        "<a href=\"" + song["url"] + "\">",
                        ", ".join(song["artists"]),
                        "–",
                        song["title"],
                        "</a",
                        "</li>"
                    ]
                html += [
                    "</ul>",
                    "</div>"
                ]
            if friend["music"].get("albums"):
                html += [
                    "<div class=\"albums\">",
                    "<strong>favourite albums:</strong>",
                    "<ul>"
                ]
                for album in friend["music"]["albums"]:
                    html += [
                        "<li>",
                        "<a href=\"" + album["url"] + "\">",
                        ", ".join(album["artists"]),
                        "–",
                        album["title"],
                        "</a",
                        "</li>"
                    ]
                html += [
                    "</ul>",
                    "</div>"
                ]
            if friend["music"].get("shows"):
                html += [
                    "<div class=\"shows\">",
                    "<strong>favourite shows:</strong>",
                    "<ul>"
                ]
                for show in friend["music"]["shows"]:
                    html += [
                        "<li>",
                        show,
                        "</li>"
                    ]
                html += [
                    "</ul>",
                    "</div>"
                ]
            if friend["music"].get("instruments"):
                html += [
                    "<div class=\"instruments\">",
                    "<strong>favourite instruments:</strong>",
                    "<ul>"
                ]
                for instrument in friend["music"]["instruments"]:
                    html += [
                        "<li>",
                        instrument,
                        "</li>"
                    ]
                html += [
                    "</ul>"
                ]
            html += [
                "</div>"
            ]
        if friend.get("books"):
            html += [
                "<div class=\"books\">",
                "<strong>favourite books:</strong>",
                "<ul>"
            ]
            for book in friend["books"]:
                html += [
                    "<li>",
                    "<a href=\"" + book["url"] + "\">",
                    book["author"],
                    "–",
                    book["title"],
                    "</a>"
                    "</li>"
                ]
            html += [
                "</ul>",
                "</div>"
            ]
        if friend.get("tv"):
            html += [
                "<div class=\"tv\">",
                "<strong>favourite TV shows:</strong>",
                "<ul>"
            ]
            for show in friend["tv"]:
                html += [
                    "<li>",
                    "<a href=\"" + show["url"] + "\">",
                    show["title"],
                    "</a>"
                    "</li>"
                ]
            html += [
                "</ul>",
                "</div>"
            ]
        if friend.get("movies"):
            html += [
                "<div class=\"movies\">",
                "<strong>favourite movies:</strong>",
                "<ul>"
            ]
            for movie in friend["movies"]:
                html += [
                    "<li>",
                    "<a href=\"" + movie["url"] + "\">",
                    movie["title"],
                    "</a>"
                    "</li>"
                ]
            html += [
                "</ul>",
                "</div>"
            ]
        if friend.get("style"):
            style = friend["style"]
            if friend["style"].get("accessories"):
                html += [
                    "<div class=\"accessories\">",
                    "<strong>favourite accessories:</strong>",
                    "<ul>"
                ]
                for accessory in style["accessories"]:
                    html += [
                        "<li>",
                        accessory,
                        "</li>"
                    ]
                html += [
                    "</ul>",
                    "</div>"
                ]
            if friend["style"].get("wardrobeItems"):
                html += [
                    "<div class=\"wardrobe-items\">",
                    "<strong>favourite wardrobe items:</strong>",
                    "<ul>"
                ]
                for item in style["wardrobeItems"]:
                    html += [
                        "<li>",
                        item,
                        "</li>"
                    ]
                html += [
                    "</ul>",
                    "</div>"
                ]
            if friend["style"].get("makeUp"):
                html += [
                    "<div class=\"make-up\">",
                    "<strong>favourite make-up:</strong>",
                    "<ul>"
                ]
                for item in style["makeUp"]:
                    html += [
                        "<li>",
                        item,
                        "</li>"
                    ]
                html += [
                    "</ul>",
                    "</div>"
                ]
            if friend["style"].get("stores"):
                html += [
                    "<div class=\"stores\">",
                    "<strong>favourite stores:</strong>",
                    "<ul>"
                ]
                for store in style["stores"]:
                    html += [
                        "<li>",
                        store,
                        "</li>"
                    ]
                html += [
                    "</ul>",
                    "</div>"
                ]
            if friend["style"].get("piercings"):
                html += [
                    "<div class=\"piercings\">",
                    "<strong>piercings:</strong>",
                    "<ul>"
                ]
                for piercing in style["piercings"]:
                    html += [
                        "<li>",
                        piercing,
                        "</li>"
                    ]
                html += [
                    "</ul>",
                    "</div>"
                ]
            if friend["style"].get("tattoos"):
                html += [
                    "<div class=\"tattoos\">",
                    "<strong>tattoos:</strong>",
                    "<ul>"
                ]
                for tattoo in style["tattoos"]:
                    html += [
                        "<li>",
                        tattoo,
                        "</li>"
                    ]
                html += [
                    "</ul>",
                    "</div>"
                ]
        if friend.get("tech"):
            html += [
                "<div class=\"tech\">"
            ]
            if friend["tech"].get("desktopOs"):
                html += [
                    "<div class=\"desktop-os\">"
                    "<strong>preferred desktop OS:</strong>",
                    friend["tech"]["desktopOs"],
                    "</div>"
                ]
            if friend["tech"].get("mobileOs"):
                html += [
                    "<div class=\"mobile-os\">"
                    "<strong>preferred mobile OS:</strong>",
                    friend["tech"]["mobileOs"],
                    "</div>"
                ]
            if friend["tech"].get("browser"):
                html += [
                    "<div class=\"browser\">"
                    "<strong>preferred browser:</strong>",
                    friend["tech"]["browser"],
                    "</div>"
                ]
            if friend["tech"].get("editor"):
                html += [
                    "<div class=\"editor\">"
                    "<strong>preferred editor:</strong>",
                    friend["tech"]["editor"],
                    "</div>"
                ]
            html += [
                "</div>"
            ]
        if friend.get("sportsTeams"):
            html += [
                "<div class=\"sports-teams\">",
                "<strong>favourite sports teams:</strong>",
                "<ul>"
            ]
            for team in friend["sportsTeams"]:
                html += [
                    "<li>",
                    team,
                    "</li>"
                ]
            html += [
                "</ul>",
                "</div>"
            ]
        if friend.get("likes"):
            html += [
                "<div class=\"likes\">",
                "<strong>likes:</strong>",
                "<ul>"
            ]
            for item in friend["likes"]:
                html += [
                    "<li>",
                    item,
                    "</li>"
                ]
            html += [
                "</ul>",
                "</div>"
            ]
        if friend.get("dislikes"):
            html += [
                "<div class=\"dislikes\">",
                "<strong>dislikes:</strong>",
                "<ul>"
            ]
            for item in friend["dislikes"]:
                html += [
                    "<li>",
                    item,
                    "</li>"
                ]
            html += [
                "</ul>",
                "</div>"
            ]
        if friend.get("hobbies"):
            html += [
                "<div class=\"hobbies\">",
                "<strong>hobbies:</strong>",
                "<ul>"
            ]
            for hobby in friend["hobbies"]:
                html += [
                    "<li>",
                    hobby,
                    "</li>"
                ]
            html += [
                "</ul>",
                "</div>"
            ]
        if friend.get("workedAt"):
            html += [
                "<div class=\"worked-at\">",
                "<strong>worked at:</strong>",
                "<ul>"
            ]
            for job in friend["workedAt"]:
                html += [
                    "<li>",
                    job["position"],
                    "at",
                    "<a href=\"" + job["url"] + "\">",
                    job["name"],
                    "</a>"
                ]
                time = job.get("time")
                if time:
                    if time[1]:
                        html += [
                            "(" + str(time[0]) + "–" + str(time[1]) + ")"
                        ]
                    else:
                        html += [
                            "(since " + str(time[0]) + ")"
                     ]
                html += [
                    "</li>"
                ]
            html += [
                "</ul>",
                "</div>"
            ]
        if friend.get("hometown"):
            html += [
                "<div class=\"hometown\">",
                "<strong>hometown:</strong>"
            ]
            place = friend["hometown"]
            place_str = ""
            if place.get("city"):
                place_str += place["city"]
            if place.get("state"):
                if place_str:
                    place_str += ", " + place["state"]
                else:
                    place_str = place["state"]
            if place.get("country"):
                if place_str:
                    place_str += " ("
                    place_str += "".join([
                        chr(ord(c) + flag_offset) for c in place["country"]
                    ])
                    place_str += ")"
                else:
                    place_str = "".join([
                        chr(ord(c) + flag_offset) for c in place["country"]
                    ])
            html += [
                place_str,
                "</div>"
            ]
        if friend.get("currentLocation"):
            html += [
                "<div class=\"current-location\">",
                "<strong>current location:</strong>"
            ]
            place = friend["currentLocation"]
            place_str = ""
            if place.get("city"):
                place_str += place["city"]
            if place.get("state"):
                if place_str:
                    place_str += ", " + place["state"]
                else:
                    place_str = place["state"]
            if place.get("country"):
                if place_str:
                    place_str += " ("
                    place_str += "".join([
                        chr(ord(c) + flag_offset) for c in place["country"]
                    ])
                    place_str += ")"
                else:
                    place_str = "".join([
                        chr(ord(c) + flag_offset) for c in place["country"]
                    ])
            html += [
                place_str,
                "</div>"
            ]
        if friend.get("livedIn"):
            html += [
                "<div class=\"lived-in\">",
                "<strong>lived in:</strong>",
                "<ul>"
            ]
            for place in friend["livedIn"]:
                place_str = ""
                if place.get("city"):
                    place_str += place["city"]
                if place.get("state"):
                    if place_str:
                        place_str += ", " + place["state"]
                    else:
                        place_str = place["state"]
                if place.get("country"):
                    if place_str:
                        place_str += " ("
                        place_str += "".join([
                            chr(ord(c) + flag_offset) for c in place["country"]
                        ])
                        place_str += ")"
                    else:
                        place_str = "".join([
                            chr(ord(c) + flag_offset) for c in place["country"]
                        ])
                html += [
                    "<li>",
                    place_str,
                    "</li>"
                ]
            html += [
                "</ul>",
                "</div>"
            ]
        if friend.get("trips"):
            html += [
                "<div class=\"trips\">",
                "<strong>favourite trips:</strong>",
                "<ul>"
            ]
            for trip in friend["trips"]:
                html += [
                    "<li>",
                    trip,
                    "</li>"
                ]
            html += [
                "</ul>",
                "</div>"
            ]
        if friend.get("modesOfTransport"):
            html += [
                "<div class=\"modes-of-transport\">",
                "<strong>favourite modes of transport:</strong>",
                "<ul>"
            ]
            for mot in friend["modesOfTransport"]:
                html += [
                    "<li>",
                    mot,
                    "</li>"
                ]
            html += [
                "</ul>",
                "</div>"
            ]
        if friend.get("languages"):
            html += [
                "<div class=\"languages\">",
                "<strong>languages spoken:</strong>",
                "<ul>"
            ]
            for language in friend["languages"]:
                html += [
                    "<li>",
                    language,
                    "</li>"
                ]
            html += [
                "</ul>",
                "</div>"
            ]
        html += [
            "<div class=\"general-info\">"
        ]
        if friend.get("ethnicity"):
            html += [
                "<div class=\"ethnicity\">",
                "<strong>ethnicity:</strong>",
                friend["ethnicity"],
                "</div>"
            ]
        if friend.get("sexuality"):
            html += [
                "<div class=\"sexuality\">",
                "<strong>sexuality:</strong>",
                friend["sexuality"],
                "</div>"
            ]
        if friend.get("genderIdentity"):
            html += [
                "<div class=\"gender-identity\">",
                "<strong>gender identity:</strong>",
                friend["genderIdentity"],
                "</div>"
            ]
        if friend.get("politicalViews"):
            html += [
                "<div class=\"political-views\">",
                "<strong>political views:</strong>",
                friend["politicalViews"],
                "</div>"
            ]
        html += [
            "</div>"
        ]
        if friend.get("mottos"):
            html += [
                "<div class=\"mottos\">",
                "<strong>mottos:</strong>",
                "<ul>"
            ]
            for motto in friend["mottos"]:
                html += [
                    "<li>",
                    motto,
                    "</li>"
                ]
            html += [
                "</ul>",
                "</div>"
            ]
        if friend.get("relationship"):
            rel = friend["relationship"]
            html += [
                "<div class=\"relationship\">",
                "<strong>relationship status:</strong>",
                rel["status"],
                "<a href=\"#" + rel["friendId"] + "\">",
                id_to_friend.get(rel["friendId"], ""),
                "</a>",
                "</div>"
            ]
        if friend.get("friendship"):
            fs = friend["friendship"]
            if fs.get("whenWeMet"):
                html += [
                    "<div class=\"when-we-met\">",
                    "<strong>when we met:</strong>",
                    fs["whenWeMet"],
                    "</div>"
                ]
            if fs.get("whereWeMet"):
                html += [
                    "<div class=\"where-we-met\">",
                    "<strong>where we met:</strong>",
                    fs["whereWeMet"],
                    "</div>"
                ]
            if fs.get("howWeMet"):
                html += [
                    "<div class=\"how-we-met\">",
                    "<strong>how we met:</strong>",
                    fs["howWeMet"],
                    "</div>"
                ]
            if fs.get("tellYou"):
                html += [
                    "<div class=\"tell-you\">",
                    "<strong>what I want to tell you:</strong>",
                    "<ul>"
                ]
                for tell_you in fs["tellYou"]:
                    html += [
                        "<li>",
                        tell_you,
                        "</li>"
                    ]
                html += [
                    "</ul>",
                    "</div>"
                ]
            if fs.get("wannaDo"):
                html += [
                    "<div class=\"wanna-do\">",
                    "<strong>what I want to do with you:</strong>",
                    "<ul>"
                ]
                for wanna_do in fs["wannaDo"]:
                    html += [
                        "<li>",
                        wanna_do,
                        "</li>"
                    ]
                html += [
                    "</ul>",
                    "</div>"
                ]
            if fs.get("memories"):
                html += [
                    "<div class=\"memories\">",
                    "<strong>memories we've shared:</strong>",
                    "<ul>"
                ]
                for memory in fs["memories"]:
                    html += [
                        "<li>",
                        memory,
                        "</li>"
                    ]
                html += [
                    "</ul>",
                    "</div>"
                ]
            if fs.get("places"):
                html += [
                    "<div class=\"places\">",
                    "<strong>places we hung out:</strong>",
                    "<ul>"
                ]
                for place in fs["places"]:
                    html += [
                        "<li>",
                        place,
                        "</li>"
                    ]
                html += [
                    "</ul>",
                    "</div>"
                ]
            if fs.get("quotes"):
                html += [
                    "<div class=\"quotes\">",
                    "<strong>my favourite quotes from you:</strong>",
                    "<ul>"
                ]
                for quote in fs["quotes"]:
                    html += [
                        "<li>",
                        quote,
                        "</li>"
                    ]
                html += [
                    "</ul>",
                    "</div>"
                ]
            if fs.get("chats"):
                html += [
                    "<div class=\"chats\">",
                    "<strong>my favourite chats with you:</strong>",
                    "<ul>"
                ]
                for chat in fs["chats"]:
                    if type(chat) is list:
                        html += [
                            "<li>",
                            "<ul>"
                        ]
                        for line in chat:
                            html += [
                                "<li>",
                                line,
                                "</li>"
                            ]
                        html += [
                            "</ul>",
                            "</li>"
                        ]
                    else:
                        html += [
                            "<li>",
                            "<img src=\"" + chat + "\">",
                            "</li>"
                        ]
                html += [
                    "</ul>",
                    "</div>"
                ]
            if fs.get("taughtMe"):
                html += [
                    "<div class=\"taught-me\">",
                    "<strong>what you taught me:</strong>",
                    "<ul>"
                ]
                for taught_me in fs["taughtMe"]:
                    html += [
                        "<li>",
                        taught_me,
                        "</li>"
                    ]
                html += [
                    "</ul>",
                    "</div>"
                ]
            if fs.get("taughtThem"):
                html += [
                    "<div class=\"taught-them\">",
                    "<strong>what I taught you:</strong>",
                    "<ul>"
                ]
                for taught_them in fs["taughtThem"]:
                    html += [
                        "<li>",
                        taught_them,
                        "</li>"
                    ]
                html += [
                    "</ul>",
                    "</div>"
                ]
        html += [
            "</div>",
            "</details>"
        ]

with open(os.path.join("friends", "friendbook.html"), "w") as file:
    file.write("\n".join(html))
