// Function to handle logout
function logout() {
    localStorage.removeItem('access_token'); // Remove token from localStorage
    window.location.href = "index.html"; // Redirect to login page
}

// Function to fetch data from the API
function fetchData(apiUrl, renderFunction) {
    const token = localStorage.getItem('access_token'); // Get token from localStorage

    if (!token) {
        alert('You must be logged in to view this page.');
        return;
    }

    fetch(apiUrl, {
        method: 'GET',
        headers: {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + token
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.status_code === 200) {
                renderFunction(data.body);
            } else {
                alert("Error fetching data: " + data.status_msg);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Function to render events table
function renderEventsTable(events) {
    const tableContainer = document.getElementById('tableContainer');
    let tableHTML = `
        <table>
            <thead>
                <tr>
                    <th>Event Name</th>
                    <th>Description</th>
                    <th>Location</th>
                    <th>Date</th>
                    <th>Attendees</th>
                </tr>
            </thead>
            <tbody>
    `;

    events.forEach(event => {
        tableHTML += `
            <tr>
                <td>${event.name}</td>
                <td>${event.description}</td>
                <td>${event.location}</td>
                <td>${new Date(event.date * 1000).toLocaleDateString()}</td>
                <td>${event.attendees.join(', ')}</td>
            </tr>
        `;
    });

    tableHTML += `</tbody></table>`;
    tableContainer.innerHTML = tableHTML;
}

// Function to render tasks table
function renderTasksTable(tasks) {
    const tableContainer = document.getElementById('tableContainer');
    let tableHTML = `
        <table>
            <thead>
                <tr>
                    <th>Task Name</th>
                    <th>Deadline</th>
                    <th>Status</th>
                    <th>Attendees</th>
                    <th>Event ID</th>
                </tr>
            </thead>
            <tbody>
    `;

    tasks.forEach(task => {
        tableHTML += `
            <tr>
                <td>${task.name}</td>
                <td>${new Date(task.deadline * 1000).toLocaleDateString()}</td>
                <td>${task.status}</td>
                <td>${task.attendees.join(', ')}</td>
                <td>${task.event_id}</td>
            </tr>
        `;
    });

    tableHTML += `</tbody></table>`;
    tableContainer.innerHTML = tableHTML;
}

// Function to render attendees table
function renderAttendeesTable(attendees) {
    const tableContainer = document.getElementById('tableContainer');
    let tableHTML = `
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Phone Number</th>
                    <th>Email</th>
                </tr>
            </thead>
            <tbody>
    `;

    attendees.forEach(attendee => {
        tableHTML += `
            <tr>
                <td>${attendee.name}</td>
                <td>${attendee.phoneNumber}</td>
                <td>${attendee.email}</td>
            </tr>
        `;
    });

    tableHTML += `</tbody></table>`;
    tableContainer.innerHTML = tableHTML;
}

// Event listener for Events link
document.getElementById('eventsLink').addEventListener('click', function () {
    document.getElementById('mainContent').innerHTML = '<h1>Events</h1><div id="tableContainer"></div>';
    fetchData('http://127.0.0.1:5000/events', renderEventsTable);
});

// Event listener for Tasks link
document.getElementById('tasksLink').addEventListener('click', function () {
    document.getElementById('mainContent').innerHTML = '<h1>Tasks</h1><div id="tableContainer"></div>';
    fetchData('http://127.0.0.1:5000/tasks', renderTasksTable);
});

// Event listener for Attendees link
document.getElementById('attendeesLink').addEventListener('click', function () {
    document.getElementById('mainContent').innerHTML = '<h1>Attendees</h1><div id="tableContainer"></div>';
    fetchData('http://127.0.0.1:5000/attendees', renderAttendeesTable);
});
