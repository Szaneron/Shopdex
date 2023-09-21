const active_link = document.getElementById('link_stock_item')
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


const increaseModal = document.getElementById('increaseModal');
const increaseModalButton = document.getElementById('stock-item-increase-button');

const reduceModal = document.getElementById('reduceModal');
const reduceModalButton = document.getElementById('stock-item-reduce-button');


const editModal = document.getElementById('editModal');
const editModalButton = document.getElementById('stock_item_edit_button');

increaseModalButton.addEventListener('click', () => {
    increaseModal.style.display = 'block';
});

reduceModalButton.addEventListener('click', () => {
    reduceModal.style.display = 'block';
});

editModalButton.addEventListener('click', () => {
    editModal.style.display = 'block';
})

// Get the <span> element that closes the modal
const closeButtons = document.querySelectorAll('.close-form');

closeButtons.forEach(closeButton => {
    closeButton.addEventListener('click', () => {
        const parentModal = closeButton.closest('.modal');
        parentModal.style.display = 'none';
    });
});

// When the user clicks anywhere outside the modal, close it
window.onclick = function (event) {
    if (event.target === increaseModal) {
        increaseModal.style.display = 'none';
    } else if (event.target === reduceModal) {
        reduceModal.style.display = 'none';
    } else if (event.target === editModal) {
        editModal.style.display = 'none';
    }
}

function confirmDeleteStockItem() {
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
                    url: `/stock_item/${stock_item_id}/`,
                    data: {
                        csrfmiddlewaretoken: token,
                        stock_item_delete: "stock_item_delete",
                    },
                    success: function () {
                        window.location.href = "/stock_item/";
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