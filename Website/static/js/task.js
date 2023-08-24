const active_link = document.getElementById('link_task')
active_link.className = 'active'

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
const renderCalendar = () => {
    let firstDayofMonth = new Date(currYear, currMonth, 0).getDay(), // getting first day of month
        lastDateofMonth = new Date(currYear, currMonth + 1, 0).getDate(), // getting last date of month
        lastDayofMonth = new Date(currYear, currMonth, lastDateofMonth).getDay(), // getting last day of month
        lastDateofLastMonth = new Date(currYear, currMonth, 0).getDate(); // getting last date of previous month
    console.log(lastDayofMonth)
    let liTag = "";
    for (let i = firstDayofMonth; i > 0; i--) { // creating li of previous month last days
        liTag += `<li class="inactive">${lastDateofLastMonth - i + 1}</li>`;
    }
    for (let i = 1; i <= lastDateofMonth; i++) { // creating li of all days of current month
        // adding active class to li if the current day, month, and year matched
        let isToday = i === date.getDate() && currMonth === new Date().getMonth()
        && currYear === new Date().getFullYear() ? "active" : "";
        liTag += `<li class="${isToday}">${i}</li>`;
    }
    for (let i = lastDayofMonth; i < 7; i++) { // creating li of next month first days
        liTag += `<li class="inactive">${i - lastDayofMonth + 1}</li>`
    }
    currentDate.innerText = `${months[currMonth]} ${currYear}`; // passing current mon and yr as currentDate text
    daysTag.innerHTML = liTag;
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

const daysList = document.querySelector('.days');
const days = daysList.querySelectorAll('li:not(.inactive)');

days.forEach(day => {
    day.addEventListener('click', () => {
        // Remove active class from previous active day
        const activeDay = daysList.querySelector('.active');
        if (activeDay) {
            activeDay.classList.remove('active');
        }

        // Add active class to the clicked day
        day.classList.add('active');

        // Send the selected date to Django view using AJAX
        const selectedDay = day.textContent;
        const selectedMonth = document.getElementById('selected-month').textContent
        console.log(selectedMonth)
        $.ajax({
            type: "POST",
            url: "",
            data: {
                csrfmiddlewaretoken: token,
                selected_day: selectedDay,
                selected_month: selectedMonth,
            },
            success: function (data) {
                const filteredTable = $('#tasks-table-content');
                filteredTable.empty();

                for (const task of data.filtered_tasks) {
                    const row = $('<tr></tr>');
                    row.append($('<td>').text(task.name));
                    row.append($('<td>').text(task.description));
                    if (task.status === 'Do zrobienia')
                        row.append($('<td class="primary">').text(task.status));
                    else if (task.status === 'Zrobione')
                        row.append($('<td class="success">').text(task.status));

                    filteredTable.append(row);
                }
            }
        });
    });
});