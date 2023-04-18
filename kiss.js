/* auto age: thanks Andre Snede for the code snippet https://stackoverflow.com/a/21984136 */

for (const xAge of document.querySelectorAll('x-age')) {
    var birthday = new Date(xAge.dataset.bday);
    var now = Date.now();
    xAge.innerHTML = Math.abs(new Date(now - birthday).getUTCFullYear() - 1970);
}

/* music (using Songwhip) */

for (const xMusic of document.querySelectorAll('a[data-music-url]')) {
    var songwhipBase = "https://songwhip.com/convert?url=";
    var songUri = encodeURIComponent(xMusic.dataset.musicUrl);
    xMusic.href = songwhipBase + songUri;
}



/*
for (const xMusic of document.querySelectorAll('x-music')) {
    const srcUrl = xMusic.dataset.url;
    const srcReq = await fetch("https://songwhip.com", {
        method: "POST",
        mode: "no-cors",
        headers: {
            "Content-Type": "application/json",
        },
        data: JSON.stringify({url: srcUrl})
    }).then((response) => {
        console.log(response);
        response.text().then((data) => {
            console.log(data);
        });
    });
//    const response = srcReq.json();
//    console.log(response);
//    console.log(srcReq.text());
}
*/
//const json = '{"type":"track","id":1524268,"path":"downers/you-dont-get-high-anymore","pagePath":"/downers/you-dont-get-high-anymore","name":"You Don\'t Get High Anymore","image":"https://is5-ssl.mzstatic.com/image/thumb/Music123/v4/b2/11/69/b21169e3-f3ac-35a0-8cdf-4ed188e55ef7/859732791423_cover.jpg/1400x1400bb.jpg","links":{"tidal":true,"amazon":true,"deezer":true,"itunes":true,"napster":true,"pandora":true,"spotify":true,"youtube":true,"amazonMusic":true,"itunesStore":true,"youtubeMusic":true},"linksCountries":["DE"],"sourceCountry":"DE","artists":[{"type":"artist","id":1072491,"path":"downers","pagePath":"/downers","name":"Downers","image":"https://is5-ssl.mzstatic.com/image/thumb/Music123/v4/b2/11/69/b21169e3-f3ac-35a0-8cdf-4ed188e55ef7/859732791423_cover.jpg/1400x1400ac.jpg","links":{"tidal":[{"link":"https://listen.tidal.com/artist/4815373","countries":["DE"]}],"amazon":[{"link":"https://amazon.de/dp/B001Q95JVO?tag=songwhip0f-21","countries":["DE"]}],"deezer":[{"link":"https://www.deezer.com/artist/561768","countries":null}],"itunes":[{"link":"https://music.apple.com/{country}/artist/downers/297435128?app=music","countries":["DE"]}],"napster":[{"link":"https://play.napster.com/artist/art.24472255","countries":null}],"spotify":[{"link":"https://open.spotify.com/artist/1bxT5W4SKk3IwnNnYsvnOB","countries":null}],"amazonMusic":[{"link":"https://music.amazon.de/artists/B001Q95JVO","countries":["DE"]}],"itunesStore":[{"link":"https://music.apple.com/{country}/artist/downers/297435128?app=itunes","countries":["DE"]}],"youtubeMusic":[{"link":"https://music.youtube.com/browse/UCIdT7HspRQZCrbdnCN_IeKw","countries":null}]},"linksCountries":["DE"],"sourceCountry":"DE","spotifyId":"1bxT5W4SKk3IwnNnYsvnOB","createdAtTimestamp":1681586303238}],"createdAtTimestamp":1681586303251,"refreshedAtTimestamp":1681586383715,"url":"https://songwhip.com/downers/you-dont-get-high-anymore"}';
//console.log(JSON.parse(json));
/*
var songwhipBase = "https://songwhip.com/convert?url=";
var songUri = encodeURIComponent("https://open.spotify.com/track/302U5SoqvU4S3zRO6cyWbV");
console.log(songwhipBase + songUri);
var response = await fetch(songwhipBase + songUri, {
    //method: 'POST',
    mode: "no-cors",
    redirect: 'follow'
});
let txt = await response.text();
console.log(txt);*/
