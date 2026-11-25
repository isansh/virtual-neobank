// Якщо користувач уже авторизований — одразу перекидаємо в кабінет
if (getToken()) {
    window.location.href = "cards.html"; // або profile.html
}

function switchTab(tab) {
    document.getElementById("tab-login").classList.toggle("active", tab === "login");
    document.getElementById("tab-register").classList.toggle("active", tab === "register");
    document.getElementById("login-form").classList.toggle("hidden", tab !== "login");
    document.getElementById("register-form").classList.toggle("hidden", tab !== "register");
}

async function handleRegister(e) {
    e.preventDefault();
    const payload = {
        full_name: document.getElementById("reg-name").value,
        email: document.getElementById("reg-email").value,
        phone_number: document.getElementById("reg-phone").value || null,
        password: document.getElementById("reg-password").value
    };

    try {
        const res = await fetch(`${API_URL}/auth/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (!res.ok) throw new Error(extractErrorMessage(data, "Помилка збереження даних"));

        showAlert("Реєстрація успішна! Тепер увійдіть у систему.");
        switchTab("login");
        document.getElementById("login-email").value = payload.email;
    } catch (err) {
        showAlert(err.message, "error");
    }
}

async function handleLogin(e) {
    e.preventDefault();
    const payload = {
        email: document.getElementById("login-email").value,
        password: document.getElementById("login-password").value
    };

    try {
        const res = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (!res.ok) throw new Error(extractErrorMessage(data, "Помилка авторизації"));

        localStorage.setItem("token", data.access_token);
        // Перехід на сторінку профілю після входу
        window.location.href = "profile.html";
    } catch (err) {
        showAlert(err.message, "error");
    }
}