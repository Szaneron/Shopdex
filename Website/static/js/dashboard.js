let months = [];
months[1] = "Styczeń";
months[2] = "Luty";
months[3] = "Marzec";
months[4] = "Kwiecień";
months[5] = "Maj";
months[6] = "Czerwiec";
months[7] = "Lipiec";
months[8] = "Sierpień";
months[9] = "Wrzesień";
months[10] = "Październik";
months[11] = "Listopad";
months[12] = "Grudzień";

let month_name = months[current_month];
document.getElementById("month-name").innerText = month_name;

let days = [];
days['Monday'] = "Poniedziałek";
days['Tuesday'] = "Wtorek";
days['Wednesday'] = "Środa";
days['Thursday'] = "Czwartek";
days['Friday'] = "Piątek";
days['Saturday'] = "Sobota";
days['Sunday'] = "Niedziela";

let day_name = days[current_day_name];
document.getElementById("day-name").innerText = day_name;

console.log(progress_bar_data_js)