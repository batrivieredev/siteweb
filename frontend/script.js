document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const logoutButton = document.getElementById('logout-button');
    const registerForm = document.getElementById('register-form');

    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            login();
        });
    }

    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            logout();
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault();
            register();
        });
    }

    if (window.location.pathname.includes('welcome.html')) {
        checkSession();
    }
});

function login() {
    let username = document.getElementById('username').value;
    let password = document.getElementById('password').value;

    fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = 'welcome.html';
        } else {
            document.getElementById('error-message').innerText = data.message;
        }
    });
}

function register() {
    let username = document.getElementById('register-username').value;
    let password = document.getElementById('register-password').value;

    fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('register-error-message').innerText = 'Inscription réussie. Vous pouvez maintenant vous connecter.';
            setTimeout(() => {
                document.getElementById('register-error-message').innerText = '';
            }, 20000); // Attendre 20 secondes avant de vider le message
        } else {
            document.getElementById('register-error-message').innerText = data.message;
        }
    });
}

function checkSession() {
    fetch('http://127.0.0.1:5000/check_session', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        if (data.logged_in) {
            document.getElementById('username').textContent = data.username;
        } else {
            window.location.href = 'index.html';
        }
    });
}

function logout() {
    fetch('http://127.0.0.1:5000/logout', {
        method: 'POST',
        credentials: 'include'
    })
    .then(() => {
        window.location.href = 'index.html';
    });
}

document.getElementById('update-button').addEventListener('click', function() {
    const newUsername = document.getElementById('new-username').value.trim();
    const newPassword = document.getElementById('new-password').value.trim();

    let data = {};
    if (newUsername) data.username = newUsername;
    if (newPassword) data.password = newPassword;

    fetch('http://127.0.0.1:5000/update_user', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (newUsername) {
                document.getElementById('username').textContent = newUsername;
                document.getElementById('username-placeholder').textContent = newUsername;
            }
            document.getElementById('settings-panel').style.display = 'none';
        } else {
            alert(data.message);
        }
    });
});

