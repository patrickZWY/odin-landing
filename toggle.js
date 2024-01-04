document.getElementById('modeToggle').addEventListener('click', function() {
    document.body.classList.toggle('dark-mode');
        if(document.body.classList.contains('dark-mode')) {
            document.querySelector('span').textContent = 'Dark Mode';
        } else {
            document.querySelector('span').textContent = 'Light Mode';
        }
});