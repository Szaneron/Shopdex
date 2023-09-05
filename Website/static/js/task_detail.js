const active_link = document.getElementById('link_task')
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

function check_if_task_is_important(value) {
    const card_element = document.getElementById(`task-card-left-id`);
    if (value === 'True') {
        card_element.style.borderLeft = '4px solid #FF0060';
    }
}

check_if_task_is_important(importnat_task);

const editModal = document.getElementById('editModal');

// Get the button that opens the modal
const openEditModal = document.getElementById('task_edit_button');

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


function confirmDeleteTask() {
    swal({
        title: "",
        text: "Czy na pewno chcesz usunąć to zadanie?",
        icon: "warning",
        buttons: true,
        dangerMode: true,
    })
        .then((willDelete) => {
            if (willDelete) {
                // After confirming, we delete the task using AJAX
                $.ajax({
                    type: "POST",
                    url: `/task/${task_id}/`,
                    data: {
                        csrfmiddlewaretoken: token,
                        task_delete: "task_delete",
                    },
                    success: function () {
                        swal("Zadanie zostało usunięte!", {
                            icon: "success",
                            timer: 3000,
                        }).then(() => {
                            window.location.href = "/dashboard/";
                        });
                    },
                    error: function (xhr, textStatus, errorThrown) {
                        console.log(xhr.status, textStatus, errorThrown);
                        swal("Wystąpił błąd podczas usuwania zadania.", {
                            icon: "error",
                            timer: 3000,
                        }).then(() => {
                            window.location.reload();
                        });
                    }
                });
            } else {
                swal("Zadanie nie zostało usunięte.", {
                    icon: "error",
                });
            }
        });
}