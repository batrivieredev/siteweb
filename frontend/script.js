document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const logoutButton = document.getElementById('logout-button');
    const registerForm = document.getElementById('register-form');
    const viewUsersButton = document.getElementById('view-users-button');
    const hideUsersButton = document.getElementById('hide-users-button');
    const userList = document.getElementById('user-list');
    const createUserButton = document.getElementById('create-user-button');
    const updateInfoButton = document.getElementById('update-info-button');
    const updateForm = document.getElementById('update-form');
    const usernameSpan = document.getElementById('username');

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

    if (updateForm) {
        updateForm.addEventListener('submit', function(event) {
            event.preventDefault();
            const newUsername = document.getElementById('new-username').value;
            const newPassword = document.getElementById('new-password').value;

            fetch('http://127.0.0.1:5000/update_user', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: newUsername, password: newPassword }),
                credentials: 'include'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    usernameSpan.innerText = newUsername;
                    alert('Informations mises à jour avec succès');
                    document.getElementById('settings-modal').style.display = 'none'; // Fermer le modal après mise à jour
                } else {
                    alert('Erreur lors de la mise à jour des informations');
                }
            });
        });
    }

    if (window.location.pathname.includes('welcome.html') || window.location.pathname.includes('welcome_user.html') || window.location.pathname.includes('welcome_admin.html')) {
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
            if (data.is_admin) {
                window.location.href = 'welcome_admin.html';
            } else {
                window.location.href = 'welcome_user.html';
            }
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

document.getElementById('update-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const newUsername = document.getElementById('new-username').value;
    const newPassword = document.getElementById('new-password').value;

    fetch('http://127.0.0.1:5000/update_user', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: newUsername || undefined,
            password: newPassword || undefined
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Informations mises à jour avec succès');
            document.getElementById('settings-modal').style.display = 'none'; // Fermer le modal après mise à jour
            document.getElementById('username').textContent = newUsername; // Mettre à jour le nom d'utilisateur en haut à droite
        } else {
            alert('Erreur lors de la mise à jour : ' + data.message);
        }
    });
});

document.getElementById('admin-update-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const currentUsername = document.getElementById('admin-update-current-username').value;
    const newUsername = document.getElementById('admin-update-new-username').value;
    const newPassword = document.getElementById('admin-update-password').value;

    fetch('http://127.0.0.1:5000/admin_update_user', {
        method: 'POST',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            current_username: currentUsername,
            new_username: newUsername || undefined,
            new_password: newPassword || undefined
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Informations mises à jour avec succès');
            document.getElementById('admin-update-modal').style.display = 'none'; // Fermer le modal après mise à jour
            fetchUsers(); // Rafraîchir la liste des utilisateurs après mise à jour
        } else {
            alert('Erreur lors de la mise à jour : ' + data.message);
        }
    });
});

document.getElementById('close-modal').addEventListener('click', function() {
    document.getElementById('settings-modal').style.display = 'none'; // Fermer le modal de mise à jour
});

document.getElementById('close-register-modal').addEventListener('click', function() {
    document.getElementById('admin-registration').style.display = 'none'; // Fermer le modal d'inscription
});

document.getElementById('close-admin-update-modal').addEventListener('click', function() {
    document.getElementById('admin-update-modal').style.display = 'none'; // Fermer le modal de mise à jour admin
});

window.addEventListener('click', function(event) {
    if (event.target == document.getElementById('settings-modal')) {
        document.getElementById('settings-modal').style.display = 'none';
    }
    if (event.target == document.getElementById('admin-registration')) {
        document.getElementById('admin-registration').style.display = 'none';
    }
    if (event.target == document.getElementById('admin-update-modal')) {
        document.getElementById('admin-update-modal').style.display = 'none';
    }
});
