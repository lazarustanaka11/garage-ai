const API_BASE = "http://127.0.0.1:8000/api";

function getToken() {
    return localStorage.getItem("access_token");
}

function setToken(token) {
    localStorage.setItem("access_token", token);
}

function removeToken() {
    localStorage.removeItem("access_token");
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
