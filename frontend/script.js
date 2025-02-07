document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const logoutButton = document.getElementById('logout-button');
    const registerForm = document.getElementById('register-form');
    const viewUsersButton = document.getElementById('view-users-button');
    const hideUsersButton = document.getElementById('hide-users-button');
    const userList = document.getElementById('user-list');
    const createUserButton = document.getElementById('create-user-button');
    const updateInfoButton = document.getElementById('update-info-button');

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

    if (viewUsersButton) {
        viewUsersButton.addEventListener('click', function() {
            fetchUsers();
        });
    }

    if (hideUsersButton) {
        hideUsersButton.addEventListener('click', function() {
            userList.style.display = 'none';
            hideUsersButton.style.display = 'none';
            viewUsersButton.style.display = 'inline-block';
        });
    }

    if (createUserButton) {
        createUserButton.addEventListener('click', function() {
            document.getElementById('admin-registration').style.display = 'block'; // Afficher le modal pour créer un nouvel utilisateur
        });
    }

    if (updateInfoButton) {
        updateInfoButton.addEventListener('click', function() {
            document.getElementById('settings-modal').style.display = 'block'; // Afficher le modal pour mettre à jour les informations
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
    let isAdmin = document.getElementById('is-admin').checked;

    fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, is_admin: isAdmin })
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
            document.getElementById('user-role').textContent = data.is_admin ? 'Administrateur' : 'Utilisateur';
            if (data.is_admin) {
                document.getElementById('create-user-button').style.display = 'inline-block';
                document.getElementById('view-users-button').style.display = 'inline-block';
            } else {
                document.getElementById('create-user-button').style.display = 'none';
                document.getElementById('view-users-button').style.display = 'none';
            }
        } else {
            window.location.href = 'index.html'; // Rediriger vers la page de connexion si non connecté
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

function fetchUsers() {
    fetch('http://127.0.0.1:5000/get_users', {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const users = document.getElementById('users');
            users.innerHTML = '';
            data.users.forEach(user => {
                const li = document.createElement('li');
                li.textContent = `${user.username} (${user.is_admin ? 'Admin' : 'User'})`;
                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Supprimer';
                deleteButton.addEventListener('click', function() {
                    deleteUser(user.username);
                });
                const updateButton = document.createElement('button');
                updateButton.textContent = 'Modifier';
                updateButton.addEventListener('click', function() {
                    openAdminUpdateModal(user.username);
                });
                li.appendChild(deleteButton);
                li.appendChild(updateButton);
                users.appendChild(li);
            });
            document.getElementById('user-list').style.display = 'block';
            document.getElementById('view-users-button').style.display = 'none';
            document.getElementById('hide-users-button').style.display = 'inline-block';
        }
    });
}

function deleteUser(username) {
    fetch('http://127.0.0.1:5000/delete_user', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            fetchUsers(); // Rafraîchir la liste des utilisateurs après suppression
        }
    });
}

function openAdminUpdateModal(username) {
    document.getElementById('admin-update-current-username').value = username;
    document.getElementById('admin-update-modal').style.display = 'block'; // Afficher le modal de mise à jour admin
}
