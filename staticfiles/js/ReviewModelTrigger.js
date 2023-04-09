const trigger = document.querySelector('#reviewModel-trigger');
const modalWrapper = document.querySelector('.reviewModel-container');
const closeBtn = document.querySelector('.reviewModel-closeBtn');

trigger.addEventListener('click', function() {
    modalWrapper.style.opacity = 1;
    modalWrapper.style.pointerEvents = 'auto' ;
});

closeBtn.addEventListener('click', function() {
    modalWrapper.style.opacity = 0;
    modalWrapper.style.pointerEvents = 'none' ;
});

modalWrapper.addEventListener('click', function(e){
    if(e.target !== this) return;
    closeModal();
});

document.addEventListener('keydown', function(e){
    if(e.key === 'Escape') {
        closeModal();
    }
})

function openModal() {
    modalWrapper.style.opacity = 1;
    modalWrapper.style.pointerEvents = 'auto' ;
}
function closeModal() {
    modalWrapper.style.opacity = 0;
    modalWrapper.style.pointerEvents = 'none' ;
}