document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const errorMessage = document.getElementById("error-message");

    // Simple form validation
    if (!username || !password) {
        errorMessage.textContent = "Please fill out both fields.";
        return;
    }

    // Make the API call to get the JWT token
    fetch('http://127.0.0.1:5000/token', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'username': username,
            'password': password
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.access_token) {
            // Store the token in localStorage
            localStorage.setItem('access_token', data.access_token);

            // Redirect to the home page
            window.location.href = "home.html";  // Example redirect
        } else {
            errorMessage.textContent = "Invalid username or password.";
        }
    })
    .catch(error => {
        errorMessage.textContent = "An error occurred. Please try again.";
        console.error('Error:', error);
    });
});
