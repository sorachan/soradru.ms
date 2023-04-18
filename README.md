# [Sora Drums' web page](https://soradru.ms) 🥁🧑‍💻

## what is this repo?

I'm a drummer and tech nerd from Germany who decided to build themselves a web presence and I've decided to use GitHub for version control and to give others a peek into how I'm building my website as I'm a huge proponent of open-source software. sharing is caring 💖

## what does this repo contain?

this repo contains the entire structure of my `~/Web/soradru.ms/` folder except for:

* the resources folders `images/` and `transcripts/`
* the `galleries/` folder with the gallery descriptors which is auto-generated
* the standalone Vue.js script which you can [download from unpkg](https://unpkg.com/vue@3/dist/vue.global.js)
* the `photoswipe/` folder, you can [download the latest release on GitHub](https://github.com/dimsemenov/PhotoSwipe/releases/latest)

## why does your website look so ugly on mobile devices?

sorry, I only bought the domain name and commenced work on 2023.3.28 and have been working full-time on the website since, just didn't get around to implementing mobile CSS yet, but I'll get it done ASAP.

in the meantime, please view the page on a 1080p+ device.

## why do you have so much random shit on your drums website?

* it's called "Sora Drums" because being a drummer is what I most identify with
    * I love the piano and other instruments, singing, CompSci, maths, and many other things as well but my life-long dream of travelling the world and playing music is more important to me than any money or other career could ever be
    and my main instrument is the drum kit
* plain and easy, I'm too lazy (for now) to maintain multiple web presences for different topics, planning on separate Instagram accounts for different topics though
    * soon™️ [@sora.drums](https://instagram.com/sora.drums) will only be used for drumming related content
    * I will reactivate my old account [@sorachanx3](https://instagram.com/sorachanx3) which has been dormant since 2017 as my main *personal* Instagram, there are some pretty cool pics on there, go check them out
    * my temporary account [@instan0body](https://instagram.com/instan0body) where I posted some drumming content a few years ago and lots of weird shit during my psychosis last year is going to be cleaned up and turned into a Tumblr-ish Instagram for content edgy teens and tweens would like
        * also got a [Tumblr](https://tumblr.com/hesflyingonbrokenwings) which I plan to clean up and use again if the platform hasn't died out by now
    * already registered [@sora.coding](https://instagram.com/sora.coding), [@sora.foodie](https://instagram.com/sora.foodie) and [@sora.education](https://instagram.com/sora.education), nothing posted yet, more to come but Instagram temporarily banned me for creating too many accs too fast lol
* this is more of a personal blog and friendbook inspired by MySpace, LiveJournal and the thousands of free website creators around 15 years ago as well as a portfolio of what I can offer gig-wise

## what is your stack?

plain HTML5 (HTML / CSS / JS), no package managers involved. those new-fangled frameworks are great for building modern web applications but they would be overkill for a simple personal webpage.

I built everything completely from scratch without any templates or includes, but decided to add:

* [Font Awesome](https://github.com/FortAwesome/Font-Awesome) for socials logos
* [Google Fonts' Raleway](https://fonts.google.com/specimen/Raleway) where the macOS system font is not available
* [PhotoSwipe](https://github.com/dimsemenov/PhotoSwipe/releases/latest) as a gallery plugin which is optimised for both traditional and touch devices
    * extended it to display caption, date, location, camera info and photography credit
    * originally only supports images, extended it to display videos and YouTube / Vimeo embeds complete with pre-load cookie / privacy disclaimer
* ~~[Vue.js](https://github.com/vuejs/core) to facilitate the programmatic creation of gallery pages~~
    * removed it when restructuring my gallery, tinkered around with JS and realised I had unintentionally already arrived at a working solution which didn't use Vue
        * my first draft of gallery organisation was horrible, didn't put enough thought into data structures
            * used folders for gallery organisation and plain text files (`.alt`, `.loc`, `.credit` etc) for metadata
            * galleries were implemented as .html include files containing HTML / Vue.js code for populating a `<div class="pswp-gallery">` element with `<a v-for=…>` children including an inline JS module to attach PhotoSwipe
            * didn't consider the use case of putting an image into multiple galleries at first, figured I'd just use filesystem links
            * this approach was ugly and unsustainable for huge amounts of photos
            * but it already supported YT / Vimeo embeds in the form of `.lnk` files
        * the second draft was much more mature
            * now organising images freely in (sub-)folders under `images/`
            * galleries are now plain text files with one image / video / embed URL per line
            * metadata, friend links and gallery association is now expressed in a single `.meta.json` file
                * decided to include a friendbook in the meantime
                * not using plain `.json` to avoid namespace conflicts with [Instaloader](https://github.com/instaloader/instaloader) and other downloader tools whose metadata I still want to parse
            * gallery population and PhotoSwipe mounting are now handled by client-side JavaScript
                * the original generated JS code from Python using lists of string literals, some with single, some with double and some with triple / sextuple quotes, some raw
                    * this was ugly as frick but it worked "for now" which was most important to me
                        * this reflects my "learning by doing" style of coding pretty well
                            * 
                        * I like the "move fast, break things" approach popularised by Facebook (not a big fan of the corporation though)
                        * my first draft is usually a poorly-thought out but working mockup using ugly hacks
                        * the second version is a cleaned-up matured version with more considerations put into data organisation, frameworks, potential problems etc
                        * this sounds counterproductive but it's actually very intuitive
                            * by making it my first goal to have a working (!) mockup I can start actually using a feature or application and gain valuable new insights on which data structures and approaches *should* have been used so I can implement the second version well-planned
                            * while this sounds like a waste of time, it's actually faster than spending hours theorising over the considerations and pitfalls that I can just as well playingly figure out this way
                        * it's not a shame to write ugly code if the situation calls for it, especially if it's only a mockup, the time for code optimisation is not always "right now" as there are often more urgent issues in a project to attend to
                        * no worries, I've learned the hard way to nonetheless comment obscure bits of code especially when working in teams, I (and probably others) have a hard time understanding some of the uncommented lines I wrote back in the day 
                * originally written using callbacks, rewritten to use `await` which is more readable and maintainable
                    * I try not to use bleeding-edge features only supported by the most recent browsers as I know people can be lazy to update or stuck on an OS which doesn't support modern browsers anymore for some reson, but I don't transpile my code for people using IE6 either (might do that if someone gives me a good reason)
            * migrated the old gallery using a simple Bash script
* toyed around with [Twemoji](https://github.com/twitter/twemoji) which replaces all emojis by platform-independent emojis but ditched it because I use emojis extensively in the `::before` styling of `<summary>` elements, and the CSS `content` property spec does not allow HTML so Twemoji failed to replace the emojs there. not their fault though and I think it's still a cool project that deserves to be mentioned.
* I use [Songwhip](https://songwhip.com) as a website to create multi-streaming links (Spotify, Apple Music, YouTube (Music), Tidal, Amazon, Soundcloud, …) for songs / artists / albums

the navigation and socials sections are stored in separate files `nav.html` and `footer.html` and are used as server-side includes: `<!--#include file="nav.html"-->`

I built a couple of helper scripts:

* `gallery-vue.py [gallery name]` generates the gallery HTML / JS includes file `galleries/[gallery name].html` for a given folder `images/[gallery name]`
    * if it finds a JSON file from Instaloader which contains metadata from the downloaded Instagram posts, it automatically adds the caption, date, location and a link to the original post
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
* [`pandoc`](https://github.com/jgm/pandoc) and [Notable](https://github.com/notable/notable) also great for easily prewriting content in markdown and then converting it to HTML, the latter is also a really useful general-purpose note-taking app. just forget to use them all the time and write HTML code directly instead, probably out of habit xD
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