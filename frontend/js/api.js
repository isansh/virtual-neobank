const API_URL = "http://127.0.0.1:8000/api";

function getToken() {
    return localStorage.getItem("token");
}

function getAuthHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${getToken()}`
    };
}

function requireAuth() {
    if (!getToken()) {
        window.location.href = "index.html";
    }
}

async function logout() {
    const token = getToken();
    if (token) {
        try {
            await fetch(`${API_URL}/auth/logout`, {
                method: "POST",
                headers: getAuthHeaders()
            });
        } catch (e) {
            console.error("Logout error:", e);
        }
    }
    localStorage.removeItem("token");
    window.location.href = "index.html";
}

function showAlert(message, type = "success") {
    const alertBox = document.getElementById("alert-box");
    if (!alertBox) return;
    alertBox.textContent = message;
    alertBox.className = `alert ${type}`;
    setTimeout(() => alertBox.classList.add("hidden"), 5000);
}

// Універсальний витягувач тексту помилки
function extractErrorMessage(data, fallback = "Сталася помилка") {
    if (!data || !data.detail) return fallback;
    if (typeof data.detail === "string") return data.detail;
    if (Array.isArray(data.detail)) {
        return data.detail.map(err => err.msg || JSON.stringify(err)).join(". ");
    }
    return fallback;
}