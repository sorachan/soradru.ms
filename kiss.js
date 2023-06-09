/* auto age: thanks Andre Snede for the code snippet https://stackoverflow.com/a/21984136 */

for (const xAge of document.querySelectorAll('x-age')) {
    var birthday = new Date(xAge.dataset.bday);
    var now = Date.now();
    xAge.innerHTML = Math.abs(new Date(now - birthday).getUTCFullYear() - 1970);
}

/* days / weeks / months / years ago */

for (const xAgo of document.querySelectorAll('x-ago')) {
    var date = new Date(xAgo.dataset.date);
    var now = new Date(Date.now());
    var dateDiff = now - date;
    if (dateDiff < 1000) {
        xAgo.innerHTML = "now";
    } else if (dateDiff < 1000 * 60) {
        xAgo.innerHTML = Math.floor(dateDiff / 1000) + "s ago";
    } else if (dateDiff < 1000 * 60 * 60) {
        xAgo.innerHTML = Math.floor(dateDiff / (1000 * 60)) + "min ago";
    } else if (dateDiff < 1000 * 60 * 60 * 24) {
        xAgo.innerHTML = Math.floor(dateDiff / (1000 * 60 * 60)) + "h ago";
    } else if (dateDiff < 1000 * 60 * 60 * 24 * 7) {
        xAgo.innerHTML = Math.floor(dateDiff / (1000 * 60 * 60 * 24)) + "d ago";
    } else if (dateDiff < 1000 * 60 * 60 * 24 * 7 * 4.348) {
        xAgo.innerHTML = Math.floor(dateDiff / (1000 * 60 * 60 * 24 * 7)) + "w ago";
    } else if (dateDiff < 1000 * 60 * 60 * 24 * 7 * 52) {
        xAgo.innerHTML = Math.floor(dateDiff / (1000 * 60 * 60 * 24 * 7 * 4.348)) + "mo ago";
    } else {
        xAgo.innerHTML = Math.floor(dateDiff / (1000 * 60 * 60 * 24 * 7 * 52.179)) + "y ago";
    }
    xAgo.title = date;
    console.log(date);
    console.log(now);
}

/* music (using Songwhip) */

for (const aMusic of document.querySelectorAll('a[data-music-url]')) {
    var songwhipBase = "https://songwhip.com/convert?url=";
    var songUri = encodeURIComponent(aMusic.dataset.musicUrl);
    aMusic.href = songwhipBase + songUri;
}