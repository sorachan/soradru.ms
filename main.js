dropdownMenus = document.querySelectorAll('.dropdown');

/* make nav button toggle nav and reset hover cooldown */

navButton = document.getElementById('nav-button');
nav = document.getElementById('nav')
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