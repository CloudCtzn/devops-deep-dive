let token = null;

function showRegister() {
    document.getElementById("login-form").style.display = "none";
    document.getElementById("register-form").style.display = "block";
}

function showLogin() {
    document.getElementById("register-form").style.display = "none";
    document.getElementById("login-form").style.display = "block";
}

function register() {
    const username = document.getElementById("reg-username").value;
    const password = document.getElementById("reg-password").value;

    fetch("/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.message) {
            alert("Account created! Please login.");
            showLogin();
        } else {
            alert("Registration failed: " + data.error);
        }
    });
}


function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch("/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password })
    })
    .then(res => res.json())
    .then(data => {
        if (data.access_token) {
            token = data.access_token;
            document.getElementById("auth-section").style.display = "none";
            document.getElementById("app-section").style.display = "block";
            loadApplications();
        } else {
            alert("Login failed");
        }
    });
}

function addApplication() {
    fetch("/applications", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify({
            company_name: document.getElementById("company").value,
            job_title: document.getElementById("title").value,
            salary: document.getElementById("salary").value,
            response: document.getElementById("status").value
        })
    })
    .then(res => res.json())
    .then(() => loadApplications());
}

function loadApplications() {
    fetch("/applications", {
        headers: { "Authorization": "Bearer " + token }
    })
    .then(res => res.json())
    .then(data => {
        const list = document.getElementById("applications-list");
        list.innerHTML = "";
        data.forEach(app => {
            list.innerHTML += `
                <div class="app-card">
                    <p><strong>${app.company_name}</strong> — ${app.job_title}</p>
                    <p>Salary: ${app.salary} | Status: ${app.response}</p>
                    <p>Date: ${app.date_submitted}</p>
                </div>
            `;
        });
    });
}

function logout() {
    token = null;
    document.getElementById("auth-section").style.display = "block";
    document.getElementById("app-section").style.display = "none";
}