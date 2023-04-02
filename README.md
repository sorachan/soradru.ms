# [Sora Drums' web page](https://soradru.ms) 🥁🧑‍💻

## what is this repo?

I'm a drummer and tech nerd from Germany who decided to build themselves a web presence and I've decided to use GitHub for version control and to give others a peek into how I'm building my website as I'm a huge proponent of open-source software. sharing is caring 💖

## what does this repo contain?

this repo contains the entire structure of my `~/Web/soradru.ms/` folder except for:

* the resources folders `images/` and `transcripts/`
* the `galleries/` folder with the gallery includes which is auto-generated
* the standalone Vue.js script which you can [download from unpkg](https://unpkg.com/vue@3/dist/vue.global.js)
* the `photoswipe/` folder, you can [download the latest release on GitHub](https://github.com/dimsemenov/PhotoSwipe/releases/latest)

## why does your website look so ugly on mobile devices?

sorry, I only bought the domain name and commenced work on 2023.3.28 and have been working full-time on the website since, just didn't get around to implementing mobile CSS yet, but I'll get it done ASAP.

in the meantime, please view the page on a 1080p+ device.

## what is your stack?

plain HTML5 (HTML / CSS / JS), no package managers involved. those new-fangled frameworks are great for building modern web applications but they would be overkill for a simple personal webpage.

I built everything completely from scratch without any templates or includes, but decided to add:

* [Font Awesome](https://github.com/FortAwesome/Font-Awesome) for socials logos
* [Google Fonts' Raleway](https://fonts.google.com/specimen/Raleway) where the macOS system font is not available
* [PhotoSwipe](https://github.com/dimsemenov/PhotoSwipe/releases/latest) as a gallery plugin which is optimised for both traditional and touch devices
    * extended it to display caption, date, location, camera info and photography credit
    * originally only supports images, extended it to display videos and YouTube / Vimeo embeds complete with pre-load cookie / privacy disclaimer
* [Vue.js](https://github.com/vuejs/core) to facilitate the programmatic creation of gallery pages
* toyed around with [Twemoji](https://github.com/twitter/twemoji) which replaces all emojis by platform-independent emojis but ditched it because I use emojis extensively in the `::before` styling of `<summary>` elements, and the CSS `content` property spec does not allow HTML so Twemoji failed to replace the emojs there. not their fault though and I think it's still a cool project that deserves to be mentioned.

the navigation and socials sections are stored in separate files `nav.html` and `footer.html` and are used as server-side includes: `<!--#include file="nav.html"-->`

I built a couple of helper scripts:

* `gallery-vue.py [gallery name]` generates the gallery HTML / JS includes file `galleries/[gallery name].html` for a given folder `images/[gallery name]`
    * if it finds a JSON file from [Instaloader](https://github.com/instaloader/instaloader) which contains metadata from the downloaded Instagram posts, it automatically adds the caption, date, location and a link to the original post
    * custom caption, date, location, camera and photography credit information can be given in `.alt`, `.date`, `.loc`, `.camera` and `.credit` files, the latter of which I create as HTML snippets in the folder `images/credits/` and link to them; the information from these files overrides information parsed from the instaloader JSON
* `get-exif.py [image file] (optional: [property])` is a helper tool for retrieving all properties or one specific property from the EXIF image metadata
* `photo-info.sh [gallery name]` is a simple console-based editor which traverses a gallery folder, displays the images and generates `.alt` and `.loc` files and `.credit` links from user input
    * it uses [pxl](https://github.com/ichinaski/pxl) to display images in the terminal which works surprisingly well if the terminal text size is small enough
    * if an instaloader caption is found, it can be copied into the `.alt` file
    * an existing caption can be:
        * appended from the top
        * appended from the bottom
        * opened in `vi`
        * replaced by a new caption
        * removed
        * left unchanged
    * if `john.doe` is input as credit info, the script will link

          "$img".credit -> images/credits/john.doe.credit

* `update-all-galleries.sh` converts all filenames in `images/` gallery folders to lower case (this helps with camera imports which use `.JPG` and other malformed extensions, so I don't have to treat them separately in my other scripts) and calls `gallery-vue.py` on each gallery

## what software do you use for development?

* my main editor is [Visual Studio Code](https://github.com/microsoft/vscode) but as a Linux enthusiast I tend to use `vi` for more complicated stuff like regex replacements or inserting in multiple lines, which I'm sure Visual Studio Code could do as well but I just didn't yet get around to learning how
* for transferring files between my laptop and my server, I just use `tar` via `nc` and `ssh` port forwards (see "Linux tips" on my website)
* I'm working on my Lenovo ThinkPad P50 "HackBook Pro" running macOS Monterey 12.6.3 which I also use for my Twitch streams (Streamlabs for video, MainStage for audio)
    * as a Linux power user (my first distro was SuSE 8.2 when I was 8 years old) I have to say I am amazed by how usable a system macOS is and think that it often gets a bad rep as a system for the unexperienced.

        I have installed macOS on my laptop on 2023.3.12 and have been using it as my main system ever since. still got my trusty X260 dual-screen setup running Manjaro on i3 in my back room which I currently use for music playback and have at my disposal if I need to do anything that would require Linux, but that case hasn't arisen yet.

        don't get me wrong, I still love Linux, my website is hosted on an Ubuntu server at my dear friend Tim's company [PHP-Friends](https://php-friends.de), it's just that a lot of stuff works out-of-the-box on macOS which is really nice, whether it be Python, bash / zsh, SSH, connecting to my NAS via NFS, controlling my back room laptop via VNC or installing developer tools the first time someone types `git` into the terminal. also, CUPS, the printer subsystem used on Linux, is maintained by Apple and is part of macOS as well, just like on Linux I can connect my cheap Brother HL-1112 monochrome laser printer to my FRITZ!Box router and use it as a network printer.

        if I need anything that macOS doesn't offer like GNU coreutils, I have [MacPorts](https://www.macports.org) and [Homebrew](https://brew.sh/) at my disposal, Windows programs can be run in [Wine Crossover](https://github.com/Gcenx/winecx).

        also, have fallen in love with their trackpad gestures, they make switching between windows / workspaces so easy and natural and let me forget that I'm working on a single screen laptop.

        some useful tools for macOS include:

        * [OpenInTerminal](https://github.com/Ji4n1ng/OpenInTerminal), a Finder extension which allows you to open folders in the Terminal or files in TextEdit
        * [KDE Connect](https://kdeconnect.kde.org), which I use to share files and clipboard contents between my Android phone and both my macOS and Linux laptops, it's also available for Windows and has a range of useful features like using your phone as a keyboard / mouse for your computer, monitoring phone battery and sending SMS from your computer, running remote commands or syncing notifications
        * [Rectangle](https://github.com/rxhanson/Rectangle), which adds snap-to-screen-border functionality for windows (if you need that, thought about downloading it but haven't yet tried it myself)

## any questions / enquiries?

feel free to:

* open an issue
* write an email to `sora+drums@dillbox.me`
* contact me on my socials / Telegram (links in footer)

[(especially if you wanna hire me as a freelance programmer!)](https://soradru.ms/coding.html)