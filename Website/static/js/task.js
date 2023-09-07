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

const daysTag = document.querySelector(".days"),
    currentDate = document.querySelector(".current-date"),
    prevNextIcon = document.querySelectorAll(".icons span");

// getting new date, current year and month
let date = new Date(),
    currYear = date.getFullYear(),
    currMonth = date.getMonth();

// storing full name of all months in array
const months = ["Styczeń", "Luty", "Marzec", "Kwiecień", "Maj", "Czerwiec", "Lipiec",
    "Sierpień", "Wrzesień", "Październik", "Listopad", "Grudzień"];

let selectedDayDate = null;

const addDayListeners = () => {
    const daysList = document.querySelector('.days');
    const days = daysList.querySelectorAll('li:not(.inactive)');

    days.forEach(day => {
        day.addEventListener('click', () => {
            // Remove active class from previous active day
            const prevActive = daysList.querySelector('.active');
            if (prevActive) {
                prevActive.classList.remove('active');
            }

            // Add the active class to the clicked day
            day.classList.add('active');
            selectedDayDate = {
                year: currYear,
                month: currMonth,
                day: parseInt(day.innerText)
            };

            // Send the selected date to Django view using AJAX
            const selectedDay = day.textContent;
            const selectedMonth = document.getElementById('selected-month').textContent
            $.ajax({
                type: "POST",
                url: "",
                data: {
                    csrfmiddlewaretoken: token,
                    selected_day: selectedDay,
                    selected_month: selectedMonth,
                },
                success: function (data) {

                    if (data.filtered_tasks.length === 0) {
                        const filteredTableThead = $('#tasks-table-content thead');
                        filteredTableThead.empty();
                        const row = $('<tr></tr>');
                        row.append($('<th>').text('Brak zadań'));

                        filteredTableThead.append(row);

                        const filteredTable = $('#tasks-table-content tbody');
                        filteredTable.hide();
                    } else {
                        const filteredTableThead = $('#tasks-table-content thead');
                        filteredTableThead.empty();

                        if (data.position === "pracownik") {
                            const row = $('<tr></tr>');
                            row.append($('<th>'));
                            row.append($('<th>').text('Nazwa'));
                            row.append($('<th>').text('Opis'));
                            row.append($('<th>').text('Status'));
                            row.append($('<th>').text(''));
                            filteredTableThead.append(row);

                            const filteredTable = $('#tasks-table-content tbody');
                            filteredTable.empty();
                            filteredTable.show();
                            for (const task of data.filtered_tasks) {
                                const row = $('<tr></tr>');

                                if (task.is_important === true) {
                                    row.append($('<td class="important">'));
                                } else {
                                    row.append($('<td>'));
                                }
                                row.append($('<td>').text(task.name))
                                row.append($('<td>').text(task.description.length > 70 ? task.description.substring(0, 70) + "..." : task.description));

                                if (task.status === 'Do zrobienia') {
                                    row.append($('<td class="primary">').text(task.status));
                                } else if (task.status === 'Zrobione') {
                                    row.append($('<td class="success">').text(task.status));
                                }

                                const detailsLinkCell = $('<td class="primary">');
                                const detailsLink = $('<a class="primary">').text('Szczegóły').attr('href', '/task/' + task.id + '/');
                                detailsLinkCell.append(detailsLink);
                                row.append(detailsLinkCell);

                                filteredTable.append(row);
                            }
                        } else {
                            const row = $('<tr></tr>');
                            row.append($('<th>'));
                            row.append($('<th>').text('Nazwa'));
                            row.append($('<th>').text('Opis'));
                            row.append($('<th>').text('Osoba'));
                            row.append($('<th>').text('Status'));
                            row.append($('<th>').text(''));
                            filteredTableThead.append(row);

                            const filteredTable = $('#tasks-table-content tbody');
                            filteredTable.empty();
                            filteredTable.show();
                            for (const task of data.filtered_tasks) {
                                const row = $('<tr></tr>');

                                if (task.is_important === true) {
                                    row.append($('<td class="important">'));
                                } else {
                                    row.append($('<td>'));
                                }
                                row.append($('<td>').text(task.name))
                                row.append($('<td>').text(task.description.length > 70 ? task.description.substring(0, 70) + "..." : task.description));

                                const imgTag = $('<img alt="" src="">').attr('src', task.assigned_to);
                                const imgCell = $('<td>').append(imgTag);
                                row.append(imgCell);

                                if (task.status === 'Do zrobienia') {
                                    row.append($('<td class="primary">').text(task.status));
                                } else if (task.status === 'Zrobione') {
                                    row.append($('<td class="success">').text(task.status));
                                }

                                const detailsLinkCell = $('<td class="primary">');
                                const detailsLink = $('<a class="primary">').text('Szczegóły').attr('href', '/task/' + task.id + '/');
                                detailsLinkCell.append(detailsLink);
                                row.append(detailsLinkCell);

                                filteredTable.append(row);
                            }

                        }
                    }
                }
            });
        });
    });
}


const renderCalendar = () => {
    let firstDayofMonth = new Date(currYear, currMonth, 0).getDay(), // getting first day of month
        lastDateofMonth = new Date(currYear, currMonth + 1, 0).getDate(), // getting last date of month
        lastDayofMonth = new Date(currYear, currMonth, lastDateofMonth).getDay(), // getting last day of month
        lastDateofLastMonth = new Date(currYear, currMonth, 0).getDate(); // getting last date of previous month

    let liTag = "";
    for (let i = firstDayofMonth; i > 0; i--) { // creating li of previous month last days
        liTag += `<li class="inactive">${lastDateofLastMonth - i + 1}</li>`;
    }
    for (let i = 1; i <= lastDateofMonth; i++) { // creating li of all days of current month
        liTag += `<li>${i}</li>`;
    }
    for (let i = lastDayofMonth; i < 7; i++) { // creating li of next month first days
        liTag += `<li class="inactive">${i - lastDayofMonth + 1}</li>`
    }


    currentDate.innerText = `${months[currMonth]} ${currYear}`; // passing current mon and yr as currentDate text
    daysTag.innerHTML = liTag;
    addDayListeners();

    if (selectedDayDate && selectedDayDate.month === currMonth && selectedDayDate.year === currYear) {
        const days = document.querySelectorAll('.days li:not(.inactive)');
        days.forEach(day => {
            if (parseInt(day.innerText) === selectedDayDate.day) {
                day.classList.add('active');
            }
        });
    } else if (selectedDayDate === null) {
        // Apply "active" class to the current day when no selected day is present
        const today = new Date();
        if (today.getFullYear() === currYear && today.getMonth() === currMonth) {
            const days = document.querySelectorAll('.days li:not(.inactive)');
            days.forEach(day => {
                if (parseInt(day.innerText) === today.getDate()) {
                    day.classList.add('active');
                }
            });
        }
    }
}
renderCalendar();

prevNextIcon.forEach(icon => { // getting prev and next icons
    icon.addEventListener("click", () => { // adding click event on both icons
        // if clicked icon is previous icon then decrement current month by 1 else increment it by 1
        currMonth = icon.id === "prev" ? currMonth - 1 : currMonth + 1;
        if (currMonth < 0 || currMonth > 11) { // if current month is less than 0 or greater than 11
            // creating a new date of current year & month and pass it as date value
            date = new Date(currYear, currMonth, new Date().getDate());
            currYear = date.getFullYear(); // updating current year with new date year
            currMonth = date.getMonth(); // updating current month with new date month
        } else {
            date = new Date(); // pass the current date as date value
        }
        renderCalendar(); // calling renderCalendar function
    });
});

