// slider
const slideContainer = document.querySelector('.aboutUs-slider-container');
const slide = document.querySelector('.slides');
const nextBtn = document.getElementById('next-btn');
const prevBtn = document.getElementById('prev-btn');
const interval = 5000;

let slides = document.querySelectorAll('.slide');
let slideIndex = 1;
let slideId;

const firstClone = slides[0].cloneNode(true);
const lastClone = slides[slides.length - 1].cloneNode(true);

firstClone.id = 'first-clone'
lastClone.id = 'last-clone'

slide.append(firstClone);
slide.prepend(lastClone);

const slideWidth = slides[slideIndex].clientWidth;
slide.style.transform = `translateX(${-slideWidth * slideIndex}px)`;

const startSlide = () => {
    slideId = setInterval(() => {
        moveToNextSlide();
    }, interval)
};

const getSlides = () => document.querySelectorAll('.slide');

slide.addEventListener('transitionend', () => {
    slides = getSlides();
    if (slides[slideIndex].id === firstClone.id) {
        slide.style.transition = 'none';
        slideIndex = 1;
        slide.style.transform = `translateX(${-slideWidth * slideIndex}px)`;
    }
    if (slides[slideIndex].id === lastClone.id) {
        slide.style.transition = 'none';
        slideIndex = slides.length - 2;
        slide.style.transform = `translateX(${-slideWidth * slideIndex}px)`;
    }
});

const moveToNextSlide = () => {
    slides = getSlides();
    if(slideIndex >= slides.length - 1) return;
    slideIndex++;
    slide.style.transform = `translateX(${-slideWidth * slideIndex}px)`;
    slide.style.transition = '1s';
};
const moveToPreviousSlide = () => {
    if(slideIndex <= 0) return;
    slideIndex--;
    slide.style.transform = `translateX(${-slideWidth * slideIndex}px)`;
    slide.style.transition = '1s';
};

slideContainer.addEventListener('mouseenter', () => {
    clearInterval(slideId);
});

slideContainer.addEventListener('mouseleave', startSlide);

nextBtn.addEventListener('click', moveToNextSlide);
prevBtn.addEventListener('click', moveToPreviousSlide);

startSlide();