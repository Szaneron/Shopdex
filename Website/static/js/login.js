const message = document.getElementById('alert-message-content');
const closeBtn = document.getElementById('close-alert');

closeBtn.addEventListener('click', () => {
    message.style.display = 'none';
});