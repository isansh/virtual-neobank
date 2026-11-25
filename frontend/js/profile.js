requireAuth();
document.addEventListener("DOMContentLoaded", loadProfile);

async function loadProfile() {
    try {
        const res = await fetch(`${API_URL}/users/me`, {
            headers: getAuthHeaders()
        });
        if (!res.ok) {
            logout();
            return;
        }
        const user = await res.json();

        document.getElementById("prof-email").value = user.email;
        document.getElementById("prof-name").value = user.full_name;
        document.getElementById("prof-phone").value = user.phone_number || "";
        document.getElementById("prof-passport").value = user.passport_number || "";
        document.getElementById("prof-tax").value = user.tax_id || "";

        const badge = document.getElementById("kyc-badge");
        if (user.kyc_status === "verified") {
            badge.textContent = "KYC Верифіковано ✓";
            badge.className = "badge verified";
        } else {
            badge.textContent = "Очікує KYC";
            badge.className = "badge pending";
        }
    } catch (err) {
        showAlert("Помилка з'єднання з сервером", "error");
    }
}

async function handleUpdateProfile(e) {
    e.preventDefault();
    const payload = {
        full_name: document.getElementById("prof-name").value,
        phone_number: document.getElementById("prof-phone").value || null,
        passport_number: document.getElementById("prof-passport").value || null,
        tax_id: document.getElementById("prof-tax").value || null
    };

    try {
        const res = await fetch(`${API_URL}/users/me`, {
            method: "PUT",
            headers: getAuthHeaders(),
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Не вдалося оновити профіль");

        showAlert("Дані профілю та KYC збережено!");
        loadProfile();
    } catch (err) {
        showAlert(err.message, "error");
    }
}

async function handleChangePassword(e) {
    e.preventDefault();
    const payload = {
        old_password: document.getElementById("old-password").value,
        new_password: document.getElementById("new-password").value
    };

    try {
        const res = await fetch(`${API_URL}/users/change-password`, {
            method: "POST",
            headers: getAuthHeaders(),
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || "Помилка зміни пароля");

        showAlert("Пароль успішно змінено!");
        document.getElementById("password-form").reset();
    } catch (err) {
        showAlert(err.message, "error");
    }
}

async function handleDeactivate() {
    if (!confirm("Ви впевнені, що хочете заблокувати акаунт? Увійти знову буде неможливо.")) return;
    
    try {
        const res = await fetch(`${API_URL}/users/deactivate`, {
            method: "POST",
            headers: getAuthHeaders()
        });
        if (res.ok) {
            alert("Акаунт заблоковано.");
            logout();
        }
    } catch (err) {
        showAlert("Помилка блокування", "error");
    }
}