// hamburger close and open
const navMenu = document.getElementById('nav-menu'),
    toggleMenu = document.getElementById('toggle-menu'),
    closeMenu = document.getElementById('close-menu')

toggleMenu.addEventListener('click', () => {
    navMenu.classList.toggle('show_menu')
})

closeMenu.addEventListener('click', () => {
    navMenu.classList.toggle('show_menu')
})

// search div toggle
const targetDiv2 = document.getElementById("searchBtn-toggle");
const btn2 = document.getElementById("searchToggle");
btn2.onclick = function () {
    if (targetDiv2.style.display !== "none") {
        targetDiv2.style.display = "none";
    } else {
        targetDiv2.style.display = "flex";
    }
};

// account div toggle
const targetDiv3 = document.getElementById("accountBtn-toggle");
const btn3 = document.getElementById("accountToggle");
btn3.onclick = function () {
    if (targetDiv3.style.display !== "none") {
        targetDiv3.style.display = "none";
    } else {
        targetDiv3.style.display = "flex";
    }
};





