const active_link = document.getElementById('link_order_item')
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

$(document).ready(function () {
    $('.change-status').click(function () {
        var itemId = $(this).data('item-id');
        var newStatus = $(this).data('status');

        $.ajax({
            type: 'POST',
            url: '',
            data: {
                change_status: 'change_status',
                item_id: itemId,
                new_status: newStatus,
                csrfmiddlewaretoken: token,
            },
            success: function () {
                swal({
                    title: "Status został zmieniony!",
                    icon: "success",
                    timer: 3000,
                }).then(() => {
                    window.location.href = "/order_item";
                });
            }
            ,
            error: function (xhr, status, error) {
                // Handle errors if needed
                console.error('Error changing status:', error);
                swal("Wystąpił błąd podczas zmiany statusu.", {
                    icon: "error",
                    timer: 3000,
                }).then(() => {
                    window.location.reload();
                });
            }
        });
    });
});

const createModal = document.getElementById('createModal');

// Get the button that opens the modal
const openCreateModal = document.getElementById('order_item_create_button');

// Get the <span> element that closes the modal
const span = document.getElementById('close-modal');

if (createModal) {
    // When the user clicks on the button, open the modal
    openCreateModal.onclick = function () {
        createModal.style.display = 'block';
    }

    // When the user clicks on <span> (x), close the modal
    span.onclick = function () {
        createModal.style.display = 'none';
    }

    // When the user clicks anywhere outside the modal, close it
    window.onclick = function (event) {
        if (event.target === createModal) {
            createModal.style.display = 'none';
        }
    }
}
