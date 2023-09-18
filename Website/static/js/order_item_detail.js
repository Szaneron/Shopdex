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

const editModal = document.getElementById('editModal');

// Get the button that opens the modal
const openEditModal = document.getElementById('order_item_edit_button');

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

const form_group_to_hide = document.getElementById('to-hide');

if (user_position === 'Pracownik') {
    form_group_to_hide.style.display = 'none';
}

function confirmDeleteOrderItem() {
    swal({
        title: "",
        text: "Czy na pewno chcesz usunąć ten produkt?",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
        .then((willDelete) => {
            if (willDelete) {
                // After confirming, we delete the task using AJAX
                $.ajax({
                    type: "POST",
                    url: `/order_item/${order_item_id}/`,
                    data: {
                        csrfmiddlewaretoken: token,
                        order_item_delete: "order_item_delete",
                    },
                    success: function () {
                        window.location.href = "/order_item/";
                        swal("Przedmiot został usunięty!", {
                            icon: "success",
                            timer: 3000,
                        })
                    },
                    error: function (xhr, textStatus, errorThrown) {
                        console.log(xhr.status, textStatus, errorThrown);
                        swal("Wystąpił błąd podczas usuwania przedmiotu.", {
                            icon: "error",
                            timer: 3000,
                        }).then(() => {
                            window.location.reload();
                        });
                    }
                });
            } else {
                swal("Przedmiot nie został usunięty.", {
                    icon: "error",
                    timer: 3000,
                });
            }
        });
}