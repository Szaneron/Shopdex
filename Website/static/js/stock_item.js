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
const reduceModal = document.getElementById('reduceModal');
const createModal = document.getElementById('createModal');

// Function to open the create modal
function openCreateModal() {
    createModal.style.display = 'block';
}

// Function to open the increase modal
function openIncreaseModal(itemId) {
    const quantityInput = document.querySelector('input[name="increase_quantity"]');
    const itemIdInput = document.querySelector('input[name="increase_item_id"]');

    quantityInput.value = '';  // Clear the previous value
    itemIdInput.value = itemId;

    increaseModal.style.display = 'block';
}

// Function to open the reduce modal
function openReduceModal(itemId, itemQuantity) {
    const quantityInput = document.querySelector('input[name="reduce_quantity"]');
    const itemIdInput = document.querySelector('input[name="reduce_item_id"]');

    quantityInput.value = '';  // Clear the previous value
    quantityInput.setAttribute('max', itemQuantity)
    itemIdInput.value = itemId;
    reduceModal.style.display = 'block';
}

const createButton = document.getElementById('stock_item_create_button');
createButton.addEventListener("click", () => {
    openCreateModal();
})

// Get all the buttons for increasing and reducing quantity
const increaseButtons = document.querySelectorAll('.increase-quantity-button');
const reduceButtons = document.querySelectorAll('.reduce-quantity-button');


increaseButtons.forEach(button => {
    button.addEventListener('click', () => {
        const itemId = button.dataset.id;
        openIncreaseModal(itemId);
    });
});

reduceButtons.forEach(button => {
    button.addEventListener('click', () => {
        const itemId = button.dataset.id;
        const itemQuantity = button.dataset.quantity
        openReduceModal(itemId, itemQuantity);
    });
});

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
    } else if (event.target === createModal) {
        createModal.style.display = 'none';
    }
}

$(document).ready(function () {
    let delayTimer;  // Timer opóźnienia

    // Function to handle AJAX search
    function performSearch() {
        let query = $('#search-input').val();
        $.ajax({
            type: 'GET',
            url: window.location.pathname,
            data: {
                q: query
            },
            success: function (data) {
                $('#stock-item-table-content').html($(data).find('#stock-item-table-content').html());

                // Hide pagination if search
                if (query !== '') {
                    $('.pagination-container').hide();
                } else {
                    $('.pagination-container').show();
                }
            }
        });
    }

    // Submit the search form via AJAX
    $('#search-input').on('input', function () {
        clearTimeout(delayTimer);  // Usuwamy poprzedni timer

        // Update search results as user types
        delayTimer = setTimeout(function () {
            performSearch();
        }, 200);  // 300 milisekund opóźnienia (możesz dostosować tę wartość)
    });

    // Obsługa zatwierdzenia formularza
    $('#search-form').on('submit', function (e) {
        e.preventDefault();  // Zapobiegamy domyślnemu zachowaniu formularza
        performSearch();  // Wywołujemy filtrowanie po zatwierdzeniu formularza
    });
});