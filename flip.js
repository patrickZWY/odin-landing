document.querySelectorAll('.type').forEach(type => {
    type.addEventListener('click', () => {
        type.classList.toggle('flipped');
    });
});