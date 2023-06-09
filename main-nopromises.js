import PhotoSwipeLightbox from "./photoswipe/dist/photoswipe-lightbox.esm.js";

const dropdownMenus = document.querySelectorAll('.dropdown');

/* make nav button toggle nav and reset hover cooldown */

const navButton = document.getElementById('nav-button');
const nav = document.getElementById('nav')
navButton.addEventListener('click', () => {
    nav.classList.toggle('open');
    for (const dropdownMenu of dropdownMenus) {
        dropdownMenu.classList.remove('cooldown');
    }
});

/* prevent accidental click on hover event */

for (const dropdownMenu of dropdownMenus) {
    dropdownMenu.addEventListener('mouseover', () => {
        setTimeout(() => {
            dropdownMenu.classList.add('cooldown');
        }, 250);
    });
}

/* PhotoSwipe galleries */

const galleries = document.querySelectorAll('.auto-pswp');
for (const gallery of galleries) {
    const galleryName = gallery.dataset.gallery;
    if (!galleryName) {
        continue;
    }
    const galleryHttp = new XMLHttpRequest();
    const galleryUrl = 'galleries/' + galleryName;
    galleryHttp.open('GET', galleryUrl);
    galleryHttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            const srcList = galleryHttp.responseText.split('\n').filter(n => n); // filter removes the empty newline at the end from the array
            const aList = [] // we need a list to fix the order of elements for the async calls return in a non-predictable order
            for (const src of srcList) {
                const a = document.createElement('a');
                aList.push(a);
                const metaJsonHttp = new XMLHttpRequest();
                const metaJsonUrl = src + '.meta.json';
                metaJsonHttp.open('GET', metaJsonUrl);
                metaJsonHttp.onreadystatechange = function () {
                    if (this.readyState == 4 && this.status == 200) {
                        const meta = JSON.parse(this.responseText);
                        a.href = src;
                        a.dataset.pswpWidth = meta.width || 0;
                        a.dataset.pswpHeight = meta.height || 0;
                        a.target = '_blank';
                        a.rel = 'noreferrer';
                        a.dataset.video = meta.video || '';
                        a.dataset.extsrc = meta.extsrc || '';
                        const img = document.createElement('img');
                        img.src = src + (meta.thumb ? '.thumb.png' : '');
                        img.alt = meta.alt || '';
                        if (meta.photoCredit) {
                            if (meta.photoCredit.friendId) {
                                const friendId = meta.photoCredit.friendId
                                const friendJsonHttp = new XMLHttpRequest();
                                const friendJsonUrl = `friends/${friendId}.json`;
                                friendJsonHttp.open('GET', friendJsonUrl);
                                friendJsonHttp.onreadystatechange = function () {
                                    if (this.readyState == 4 && this.status == 200) {
                                        const friend = JSON.parse(this.responseText);
                                        friendName = friend.general.name || '';
                                        img.dataset.credit = `<a href="friends.html#friend-${friendId}">👤 ${friendName}</a>`;
                                    }
                                }
                            } else if (meta.photoCredit.external) {
                                const creditName = meta.photoCredit.external.name || '';
                                const creditUrl = meta.photoCredit.external.url || '';
                                img.dataset.credit = `<a href="${creditUrl}">🌐 ${creditName}</a>`;
                            }
                        }
                        if (meta.camera) {
                            const make = meta.camera.make || '';
                            const model = meta.camera.model || '';
                            img.dataset.camera = `${make} ${model}`.trim();
                        }
                        if (meta.date) {
                            if (meta.date.timeString) {
                                img.dataset.date = meta.date.timeString;
                            } else if (meta.date.timeStamp) {
                                const date = new Date(meta.date.timeStamp * 1000);
                                img.dataset.date = `${date.getFullYear()}.${date.getMonth() + 1}.${date.getDate()} ${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}:${date.getSeconds().toString().padStart(2, '0')}`;
                            }
                        }
                        if (meta.location) {
                            if (meta.location.latLng) {
                                img.dataset.location = `<a href="geo:${meta.location.latLng[0]},${meta.location.latLng[1]}">${meta.location.name}</a>`;
                            } else {
                                img.dataset.location = meta.location.name || '';
                            }
                        }
                        a.appendChild(img);
                    }
                };
                metaJsonHttp.send();
            }
            for (const a of aList) {
                gallery.appendChild(a);
            }
        }
    };
    galleryHttp.send();
    const lightbox = new PhotoSwipeLightbox({
        gallery: '#' + gallery.id || '',
        children: "a",
        pswpModule: () => import("./photoswipe/dist/photoswipe.esm.js")
    });
    lightbox.on('uiRegister', function() {
        lightbox.pswp.ui.registerElement({
            name: 'custom-caption',
            isButton: false,
            appendTo: 'root',
            onInit: (el, pswp) => {
            lightbox.pswp.on('change', () => {
                const currSlideElement = lightbox.pswp.currSlide.data.element;
                let captionHTML = '';
                let creditHTML = '';
                let cameraHTML = '';
                let dateHTML = '';
                let locationHTML = '';
                if (currSlideElement) {
                    captionHTML = currSlideElement.querySelector('img').getAttribute('alt');
                    creditHTML = currSlideElement.querySelector('img').getAttribute('data-credit');
                    cameraHTML = currSlideElement.querySelector('img').getAttribute('data-camera');
                    dateHTML = currSlideElement.querySelector('img').getAttribute('data-date');
                    locationHTML = currSlideElement.querySelector('img').getAttribute('data-location');
                }
                el.innerHTML = '';
                if (captionHTML) {
                    el.innerHTML += '<div class="photo-caption">' + captionHTML + '</div>';
                }
                if (cameraHTML) {
                    el.innerHTML += '<div class="photo-camera">' + cameraHTML + '</div>';
                }
                if (creditHTML) {
                    el.innerHTML += '<div class="photo-credit">' + creditHTML + '</div>';
                }
                if (dateHTML) {
                    el.innerHTML += '<div class="photo-date">' + dateHTML + '</div>';
                }
                if (locationHTML) {
                    el.innerHTML += '<div class="photo-location">' + locationHTML + '</div>';
                }
            });}
        });
    });
    lightbox.addFilter('itemData', (itemData, index) => {
        const video = itemData.element.dataset.video;
        const extsrc = itemData.element.dataset.extsrc;
        if (video) {
            itemData.video = video;
        }
        if (extsrc) {
            itemData.extsrc = extsrc;
        }
        return itemData;
    });
    lightbox.on('contentLoad', (e) => {
        const { content, isLazy } = e;
        if (content.data.element.dataset.video) {
            content.videoDiv = document.createElement('div');
            content.videoDiv.classList.add('video-div');
            content.videoDiv.classList.add('pswp__img');
            const wrapper = document.createElement('div');
            wrapper.classList.add('video-wrapper');
            const videoElement = document.createElement('video');
            videoElement.src = content.data.element.dataset.video;
            const overlay = document.createElement('div');
            overlay.classList.add('video-overlay');
            overlay.addEventListener('click', () => {
                overlay.classList.add('playing');
                videoElement.play();
            });
            videoElement.addEventListener('click', () => {
                videoElement.pause();
                overlay.classList.remove('playing');
            });
            videoElement.addEventListener('ended', () => {
                videoElement.pause();
                overlay.classList.remove('playing');
            });
            const button = document.createElement('div');
            button.classList.add('video-button');
            button.innerHTML = '▶️';
            overlay.appendChild(button);
            wrapper.appendChild(videoElement);
            wrapper.appendChild(overlay);
            content.videoDiv.appendChild(wrapper);
            content.state = 'loading';
            content.onLoaded();
        }
        if (content.data.element.dataset.extsrc) {
            content.iframeDiv = document.createElement('div');
            content.iframeDiv.classList.add('iframe-div');
            content.iframeDiv.classList.add('pswp__img');
            const wrapper = document.createElement('div');
            wrapper.classList.add('iframe-wrapper');
            wrapper.style.width = content.data.element.dataset.pswpWidth;
            wrapper.style.height = content.data.element.dataset.pswpHeight;
            const iframeElement = document.createElement('iframe');
            iframeElement.src = content.data.element.dataset.extsrc;
            iframeElement.setAttribute('allowFullScreen', '');
            iframeElement.style.width = content.data.element.dataset.pswpWidth;
            iframeElement.style.height = content.data.element.dataset.pswpHeight;
            const overlay = document.createElement('div');
            overlay.classList.add('iframe-overlay');
            overlay.addEventListener('click', () => {
                overlay.classList.add('playing');
                wrapper.appendChild(iframeElement);
            });
            const button = document.createElement('div');
            button.classList.add('iframe-button');
            button.innerHTML = '⚠️';
            const warning = document.createElement('div');
            warning.classList.add('iframe-warning');
            warning.innerHTML = '<p>warning!</p>'
                + '<p>you are about to load an external iframe from <em>'
                + new URL(iframeElement.src).hostname
                + '</em>, by doing so you agree to their cookie and privacy policies!</p>';
            overlay.appendChild(warning);
            overlay.appendChild(button);
            wrapper.appendChild(overlay);
            content.iframeDiv.appendChild(wrapper);
            content.state = 'loading';
            content.onLoaded();
        }
    });
    lightbox.on('contentAppend', (e) => {
        const { content } = e;
        if (content.videoDiv && !content.videoDiv.parentNode) {
            e.preventDefault();
            content.slide.container.appendChild(content.videoDiv);
        }
        if (content.iframeDiv && !content.iframeDiv.parentNode) {
            e.preventDefault();
            content.slide.container.appendChild(content.iframeDiv);
        }
    });
    lightbox.on('contentRemove', (e) => {
        const { content } = e;
        if (content.videoDiv && content.videoDiv.parentNode) {
            e.preventDefault();
            content.videoDiv.remove();
        }
        if (content.iframeDiv && content.iframeDiv.parentNode) {
            e.preventDefault();
            content.iframeDiv.remove();
        }
    });
    lightbox.init();
}