const active_link = document.getElementById('link_notification')
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


document.addEventListener('DOMContentLoaded', () => {
    const markAsReadButtons = document.querySelectorAll('.mark-as-read');

    markAsReadButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const notificationId = event.target.dataset.notificationId;

            $.ajax({
                type: 'POST',
                url: '',
                data: {
                    mark_as_read: 'mark_as_read',
                    notification_id: notificationId,
                    csrfmiddlewaretoken: token,
                },
                success: function () {
                    swal({
                        title: "Powiadomienie oznaczone jako przeczytane!",
                        icon: "success",
                        timer: 3000,
                    }).then(() => {
                        window.location.reload();
                    });
                }
                ,
                error: function (xhr, status, error) {
                    // Handle errors if needed
                    console.error('Error changing status:', error);
                    swal("Wystąpił błąd podczas oznaczania powiadomienia jak przeczytane.", {
                        icon: "error",
                        timer: 3000,
                    }).then(() => {
                        window.location.reload();
                    });
                }
            });
        });
    });
});
