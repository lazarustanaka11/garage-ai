const API_BASE = "/api";

function getToken() {
    return localStorage.getItem("access_token");
}

function setToken(token) {
    localStorage.setItem("access_token", token);
    updateNavbar();
}

function removeToken() {
    localStorage.removeItem("access_token");
    updateNavbar();
}

function isLoggedIn() {
    return getToken() !== null;
}

function logout() {
    removeToken();
    window.location.href = "/login";
}

function requireLogin() {

    const protectedPages = [
        "/customers",
        "/vehicles",
        "/repair-jobs"
    ];

    const current = window.location.pathname;

    if (protectedPages.includes(current) && !isLoggedIn()) {

        window.location.href = "/login";

    }

}

async function apiRequest(endpoint, options = {}) {

    const headers = options.headers || {};

    headers["Content-Type"] = "application/json";

    const token = getToken();

    if (token) {
        headers["Authorization"] = `Bearer ${token}`;
    }

    const response = await fetch(API_BASE + endpoint, {
        ...options,
        headers,
    });

    if (response.status === 401) {

        logout();

        return;

    }

    if (!response.ok) {

        throw await response.json();

    }

    if (response.status === 204) {

        return null;

    }

    return await response.json();

}

const api = {

    get: (url) => apiRequest(url),

    post: (url, body) =>
        apiRequest(url, {
            method: "POST",
            body: JSON.stringify(body),
        }),

    put: (url, body) =>
        apiRequest(url, {
            method: "PUT",
            body: JSON.stringify(body),
        }),

    delete: (url) =>
        apiRequest(url, {
            method: "DELETE",
        }),

};

document.addEventListener("DOMContentLoaded", () => {

    requireLogin();

});
