const API_URL = "";

const elements = {
    authCard: document.getElementById("auth-card"),
    authCardButton: document.getElementById("auth-card-button"),
    authCardMessage: document.getElementById("auth-card-message"),
    authStatus: document.getElementById("auth-status"),
    currentUser: document.getElementById("current-user"),
    loginButton: document.getElementById("login-button"),
    logoutButton: document.getElementById("logout-button"),
    notification: document.getElementById("notification"),
    orders: document.getElementById("orders"),
    profileAvatar: document.getElementById("profile-avatar"),
    profileProof: document.getElementById("profile-proof"),
    profileSection: document.getElementById("profile-section"),
    products: document.getElementById("products"),
    users: document.getElementById("users"),
};

function showNotification(message, type = "info") {
    elements.notification.textContent = message;
    elements.notification.className = `notification notification-${type}`;
    elements.notification.hidden = false;
}

function setAuthStatus(message, state = "signed-out") {
    elements.authStatus.textContent = message;
    elements.authStatus.dataset.state = state;
}

function setButtonLoading(button, label) {
    button.disabled = true;
    button.dataset.originalLabel = button.textContent;
    button.innerHTML = `<span class="spinner spinner-small"></span>${label}`;
}

function restoreButton(button) {
    button.disabled = false;
    button.textContent = button.dataset.originalLabel || button.textContent;
}

function renderSignedOut(message = "Your profile and order history are protected. Sign in securely with your customer account to continue.") {
    elements.authCard.hidden = false;
    elements.profileSection.hidden = true;
    elements.authCardMessage.textContent = message;
    elements.loginButton.hidden = false;
    elements.logoutButton.hidden = true;
    elements.authCardButton.hidden = false;
    elements.authCardButton.disabled = false;
    elements.authCardButton.textContent = "Sign in securely";
    setAuthStatus("Signed out", "signed-out");
    elements.orders.innerHTML = `
        <div class="protected-state">
            <span class="lock-icon" aria-hidden="true">&#9679;</span>
            <strong>Your orders are protected</strong>
            <span>Sign in to view your personal order history.</span>
        </div>`;
}

function renderSignedIn(user) {
    const displayName = user.name || user.email || "Customer";
    const initial = displayName.trim().charAt(0).toUpperCase() || "M";
    elements.authCard.hidden = true;
    elements.profileSection.hidden = false;
    const familyName = user.family_name ? ` · Family name: ${user.family_name}` : "";
    elements.currentUser.textContent = `${displayName} · ${user.email}${familyName}`;
    elements.profileProof.textContent = user.cognito_profile_verified
        ? "Identity verified by Amazon Cognito"
        : "Signed in with Amazon Cognito";
    elements.profileAvatar.textContent = initial;
    elements.loginButton.hidden = true;
    elements.logoutButton.hidden = false;
    setAuthStatus("Signed in", "signed-in");
}

function friendlyApiMessage(response, fallback) {
    if (response.status === 401) return "Your session has expired. Please sign in again.";
    if (response.status === 403) return "You do not have permission to view this information.";
    if (response.status >= 500) return "The service is temporarily unavailable. Please try again shortly.";
    return fallback;
}

async function requestJson(path, options = {}) {
    const accessTokenPresent = Boolean(Auth.accessToken());
    let response;
    try {
        response = await fetch(`${API_URL}${path}`, {
            ...options,
            headers: { ...authenticatedHeaders(), ...(options.headers || {}) },
        });
    } catch (error) {
        if (path === "/users/me") {
            console.error("GET /users/me diagnostic", {
                accessTokenPresent,
                status: "network_error",
                response: null,
            });
        }
        throw new Error("We could not reach the dashboard service. Check your connection and try again.");
    }

    let body = {};
    try {
        body = await response.json();
    } catch (error) {
        body = {};
    }

    if (path === "/users/me") {
        console.info("GET /users/me diagnostic", {
            accessTokenPresent,
            status: response.status,
            response: safeDiagnosticBody(body),
        });
    }

    if (response.status === 401 && ["/users/me", "/orders"].includes(path)) {
        Auth.clearSession();
        const message = body.error || "Your session has expired. Please sign in again.";
        renderSignedOut(message);
        showNotification(message, "warning");
        const error = new Error(message);
        error.status = response.status;
        error.reason = body.reason;
        throw error;
    }
    return { response, body };
}

function safeDiagnosticBody(body) {
    if (!body || typeof body !== "object" || Array.isArray(body)) return null;
    const safeFields = ["error", "reason", "message", "detail", "status"];
    return Object.fromEntries(
        safeFields
            .filter(key => Object.hasOwn(body, key))
            .map(key => [key, body[key]])
    );
}

function authenticatedHeaders() {
    const token = Auth.accessToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
}

function renderLoading(container, label) {
    container.innerHTML = `<div class="loading-state"><span class="spinner"></span>${label}</div>`;
}

function renderEmpty(container, message) {
    container.innerHTML = `<div class="empty-state"><strong>${message}</strong></div>`;
}

function renderError(container, message) {
    container.innerHTML = `<div class="error-state"><strong>${message}</strong><span>Try refreshing in a moment.</span></div>`;
}

function createCard(className, content) {
    const card = document.createElement("article");
    card.className = className;
    card.innerHTML = content;
    return card;
}

function escapeHtml(value) {
    return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

async function loadProducts() {
    renderLoading(elements.products, "Loading products...");
    try {
        const { response, body } = await requestJson("/products");
        if (!response.ok || !Array.isArray(body)) {
            renderError(elements.products, friendlyApiMessage(response, "Products could not be loaded."));
            return;
        }
        if (!body.length) {
            renderEmpty(elements.products, "No products are available right now.");
            return;
        }
        elements.products.innerHTML = "";
        body.forEach(product => {
            elements.products.appendChild(createCard("data-card product-card", `
                <div class="card-topline"><span class="card-kicker">Product ${escapeHtml(product.id)}</span><span class="stock-pill">${escapeHtml(product.stock)} in stock</span></div>
                <h3>${escapeHtml(product.name)}</h3>
                <p class="price">₹${escapeHtml(product.price)}</p>
            `));
        });
    } catch (error) {
        renderError(elements.products, error.message === "AUTHENTICATION_EXPIRED" ? "Your session has expired." : error.message);
    }
}

async function loadUsers() {
    renderLoading(elements.users, "Loading customers...");
    try {
        const { response, body } = await requestJson("/users");
        if (!response.ok || !Array.isArray(body)) {
            renderError(elements.users, friendlyApiMessage(response, "Customers could not be loaded."));
            return;
        }
        if (!body.length) {
            renderEmpty(elements.users, "No customers have joined yet.");
            return;
        }
        elements.users.innerHTML = "";
        body.forEach(user => {
            elements.users.appendChild(createCard("data-card customer-card", `
                <div class="avatar-small">${escapeHtml((user.name || "C").charAt(0).toUpperCase())}</div>
                <div><h3>${escapeHtml(user.name)}</h3><p>${escapeHtml(user.email)}</p></div>
            `));
        });
    } catch (error) {
        renderError(elements.users, error.message);
    }
}

async function loadCurrentUser() {
    const { response, body } = await requestJson("/users/me");
    if (!response.ok) {
        const error = new Error(body.error || friendlyApiMessage(response, "Your profile could not be loaded."));
        error.status = response.status;
        error.reason = body.reason;
        throw error;
    }
    renderSignedIn(body);
}

async function loadOrders() {
    if (!Auth.accessToken()) {
        renderSignedOut();
        return;
    }
    renderLoading(elements.orders, "Loading your orders...");
    try {
        const { response, body } = await requestJson("/orders");
        if (!response.ok || !Array.isArray(body)) {
            renderError(elements.orders, friendlyApiMessage(response, "Your orders could not be loaded."));
            return;
        }
        if (!body.length) {
            renderEmpty(elements.orders, "You don't have any orders yet.");
            return;
        }
        elements.orders.innerHTML = "";
        body.forEach(order => {
            elements.orders.appendChild(createCard("data-card order-card", `
                <div class="order-heading"><h3>Order #${escapeHtml(order.id)}</h3><span class="status-pill">${escapeHtml(order.status)}</span></div>
                <dl class="order-details">
                    <div><dt>Product</dt><dd>#${escapeHtml(order.product_id)}</dd></div>
                    <div><dt>Quantity</dt><dd>${escapeHtml(order.quantity)}</dd></div>
                    <div><dt>Total</dt><dd>₹${escapeHtml(order.total_price)}</dd></div>
                </dl>
            `));
        });
    } catch (error) {
        if (error.message !== "AUTHENTICATION_EXPIRED") renderError(elements.orders, error.message);
    }
}

async function startSignIn(button) {
    setButtonLoading(button, "Redirecting to secure sign in...");
    setAuthStatus("Preparing secure sign in", "loading");
    showNotification("Redirecting to secure sign in...", "info");
    try {
        await Auth.login();
    } catch (error) {
        restoreButton(button);
        setAuthStatus("Signed out", "signed-out");
        showNotification(error.message, "error");
    }
}

async function initialize() {
    elements.loginButton.addEventListener("click", () => startSignIn(elements.loginButton));
    elements.authCardButton.addEventListener("click", () => startSignIn(elements.authCardButton));
    elements.logoutButton.addEventListener("click", () => Auth.logout());
    document.getElementById("refresh-products").addEventListener("click", loadProducts);
    document.getElementById("refresh-users").addEventListener("click", loadUsers);
    document.getElementById("refresh-orders").addEventListener("click", loadOrders);

    renderLoading(elements.products, "Loading products...");
    renderLoading(elements.users, "Loading customers...");
    try {
        await Auth.loadConfig();
        const callbackHandled = await Auth.exchangeCode();
        if (callbackHandled) showNotification("Finishing your secure sign in...", "info");
    } catch (error) {
        renderSignedOut(error.message);
        showNotification(error.message, "error");
    }

    await Promise.all([loadProducts(), loadUsers()]);
    if (!Auth.accessToken()) {
        renderSignedOut();
        return;
    }
    try {
        await loadCurrentUser();
        await loadOrders();
        showNotification("You are signed in and ready to go.", "success");
    } catch (error) {
        if (error.status === 401) {
            Auth.clearSession();
            renderSignedOut(error.message);
            showNotification(error.message, "warning");
            console.warn("Backend rejected the Cognito access token", {
                reason: error.reason || "unauthenticated",
                status: error.status,
            });
            return;
        }

        elements.authCard.hidden = true;
        elements.profileSection.hidden = false;
        elements.currentUser.textContent = "Your profile is temporarily unavailable.";
        elements.profileProof.textContent = "Your access token is still present; profile verification did not complete.";
        elements.loginButton.hidden = true;
        elements.logoutButton.hidden = false;
        setAuthStatus("Profile unavailable", "loading");
        showNotification(error.message || "We could not load your profile. Please try again.", "error");
        console.error("Cognito profile request failed", {
            status: error.status || "network_error",
            reason: error.reason || "profile_request_failed",
            message: error.message,
        });
    }
}

window.addEventListener("DOMContentLoaded", initialize);
