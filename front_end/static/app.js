const API_URL = "";

function setAuthStatus(message) {
    document.getElementById("auth-status").textContent = message;
}

function showAuthRequired() {
    document.getElementById("orders").textContent = "Login required to view your orders.";
    document.getElementById("current-user").textContent = "Login to view your profile and orders.";
    document.getElementById("login-button").hidden = false;
    document.getElementById("logout-button").hidden = true;
    setAuthStatus("Not authenticated");
}

function authenticatedHeaders() {
    const token = Auth.accessToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
}

async function fetchJson(path, options = {}) {
    const response = await fetch(`${API_URL}${path}`, {
        ...options,
        headers: { ...authenticatedHeaders(), ...(options.headers || {}) },
    });
    if (response.status === 401) {
        sessionStorage.removeItem("cognito_access_token");
        showAuthRequired();
        throw new Error("Authentication expired");
    }
    return { response, body: await response.json() };
}

async function loadUsers() {
    try {
        const { response, body } = await fetchJson("/users");
        const container = document.getElementById("users");
        container.innerHTML = "";
        if (!response.ok || !Array.isArray(body)) {
            container.textContent = body.error || "Unable to load users.";
            return;
        }
        if (!body.length) {
            container.textContent = "No users found.";
            return;
        }
        body.forEach(user => {
            const card = document.createElement("div");
            card.className = "card";
            card.textContent = `${user.name} | ID: ${user.id} | ${user.email}`;
            container.appendChild(card);
        });
    } catch (error) {
        document.getElementById("users").textContent = "Unable to load users.";
    }
}

async function loadProducts() {
    try {
        const { response, body } = await fetchJson("/products");
        const container = document.getElementById("products");
        container.innerHTML = "";
        if (!response.ok || !Array.isArray(body)) {
            container.textContent = body.error || "Unable to load products.";
            return;
        }
        if (!body.length) {
            container.textContent = "No products found.";
            return;
        }
        body.forEach(product => {
            const card = document.createElement("div");
            card.className = "card";
            card.textContent = `${product.name} | ID: ${product.id} | Price: ${product.price} | Stock: ${product.stock}`;
            container.appendChild(card);
        });
    } catch (error) {
        document.getElementById("products").textContent = "Unable to load products.";
    }
}

async function loadCurrentUser() {
    const { response, body } = await fetchJson("/users/me");
    if (!response.ok) throw new Error(body.error || "Unable to load profile");
    document.getElementById("current-user").textContent = `${body.name} | ${body.email}`;
    setAuthStatus(`Signed in as ${body.email}`);
    document.getElementById("login-button").hidden = true;
    document.getElementById("logout-button").hidden = false;
}

async function loadOrders() {
    if (!Auth.accessToken()) {
        showAuthRequired();
        return;
    }
    try {
        const { response, body } = await fetchJson("/orders");
        const container = document.getElementById("orders");
        container.innerHTML = "";
        if (!response.ok || !Array.isArray(body)) {
            container.textContent = body.error || "Unable to load orders.";
            return;
        }
        if (!body.length) {
            container.textContent = "No orders found.";
            return;
        }
        body.forEach(order => {
            const card = document.createElement("div");
            card.className = "card";
            card.textContent = `Order #${order.id} | Product: ${order.product_id} | Quantity: ${order.quantity} | Total: ${order.total_price} | ${order.status}`;
            container.appendChild(card);
        });
    } catch (error) {
        if (error.message !== "Authentication expired") {
            document.getElementById("orders").textContent = "Unable to load orders.";
        }
    }
}

async function initialize() {
    document.getElementById("login-button").addEventListener("click", async () => {
        try { await Auth.login(); } catch (error) { setAuthStatus(error.message); }
    });
    document.getElementById("logout-button").addEventListener("click", () => Auth.logout());
    await Auth.loadConfig();
    try { await Auth.exchangeCode(); } catch (error) { setAuthStatus(error.message); }
    await loadUsers();
    await loadProducts();
    if (Auth.accessToken()) {
        try {
            await loadCurrentUser();
            await loadOrders();
        } catch (error) {
            showAuthRequired();
        }
    } else {
        showAuthRequired();
    }
}

window.addEventListener("DOMContentLoaded", initialize);
