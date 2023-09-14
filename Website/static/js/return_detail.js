const active_link = document.getElementById('link_return')
active_link.className = 'active'

const sideMenu = document.querySelector('aside');
const menuBtn = document.getElementById('menu-btn');
const closeBtn = document.getElementById('close-btn');

// Add a click event listener to the menu button to display the side menu.
menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
});

// Add a click event listener to the close button to hide the side menu.
closeBtn.addEventListener('click', () => {
    sideMenu.style.display = '';
});


const editModal = document.getElementById('editModal');

// Get the button that opens the modal
const openEditModal = document.getElementById('return_edit_button');

// Get the <span> element that closes the modal
const span = document.getElementById('close-modal');

if (openEditModal) {
    // When the user clicks on the button, open the modal
    openEditModal.onclick = function () {
        editModal.style.display = 'block';
    }

    // When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        editModal.style.display = 'none';
    }

    // When the user clicks anywhere outside the modal, close it
    window.onclick = function (event) {
        if (event.target === editModal) {
            editModal.style.display = 'none';
        }
    }
}