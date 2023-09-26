const active_link = document.getElementById('link_admin_panel')
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

function showDefaultTab() {
    const defaultTab = document.querySelector('.tab-content .tab-pane');
    const defaultHeaderTab = document.querySelector('.tab-header .tab-item:first-child');

    defaultHeaderTab.classList.add('active');
    if (defaultTab) {
        defaultTab.style.display = 'block';
    }
}

document.addEventListener('DOMContentLoaded', showDefaultTab);

function showTab(tabName) {
    const tabItems = document.querySelectorAll('.tab-header .tab-item');
    tabItems.forEach(tabItem => {
        tabItem.classList.remove('active');
    });

    const selectedTab = document.getElementById(`${tabName}-tab-item`);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }

    // Ukryj wszystkie panele
    const tabPanes = document.querySelectorAll('.tab-content .tab-pane');
    tabPanes.forEach(tabPane => {
        tabPane.style.display = 'none';
    });

    // Pokaż wybrany panel
    const selectedTabPane = document.getElementById(`${tabName}-tab`);
    if (selectedTabPane) {
        selectedTabPane.style.display = 'block';
    }
}

// Create a chart using the retrieved data
const ctx = document.getElementById('adminChart').getContext('2d');
const chart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: monthLabels,
        datasets: [{
            label: 'Dostawy',
            data: deliveryMonthData,
            backgroundColor: '#7f6cc1',
            borderRadius: 10,
        }, {
            label: 'Zadania',
            data: tasksMonthData,
            backgroundColor: '#EFB34A',
            borderRadius: 10,
            color: '#EDB34E'
        }],
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
                labels: {
                    color: '#272B37'
                }
            }
        },
        scales: {
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    color: '#272B37',
                }
            },
            y: {
                beginAtZero: true,
                grid: {
                    display: false
                },
                ticks: {
                    color: '#272B37',
                }
            }
        }
    }
});