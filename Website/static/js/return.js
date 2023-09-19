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
                $('#received-retruns-table-content').html($(data).find('#received-retruns-table-content').html());
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