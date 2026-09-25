const Auth = (() => {
    const TOKEN_KEY = "cognito_access_token";
    const STATE_KEY = "cognito_oauth_state";
    const VERIFIER_KEY = "cognito_pkce_verifier";
    let config = null;

    function base64Url(bytes) {
        return btoa(String.fromCharCode(...new Uint8Array(bytes)))
            .replace(/\+/g, "-")
            .replace(/\//g, "_")
            .replace(/=+$/, "");
    }

    function randomString(length = 32) {
        return base64Url(crypto.getRandomValues(new Uint8Array(length)));
    }

    async function challenge(verifier) {
        const digest = await crypto.subtle.digest(
            "SHA-256",
            new TextEncoder().encode(verifier)
        );
        return base64Url(digest);
    }

    function clearCallbackParams() {
        window.history.replaceState({}, document.title, window.location.pathname);
    }

    async function loadConfig() {
        const response = await fetch("/config");
        if (!response.ok) throw new Error("Authentication settings are unavailable.");
        config = await response.json();
        return config;
    }

    async function login() {
        if (!config) await loadConfig();
        if (!config.domain || !config.clientId) {
            throw new Error("Secure sign-in is not configured yet.");
        }
        const verifier = randomString();
        const state = randomString();
        sessionStorage.setItem(VERIFIER_KEY, verifier);
        sessionStorage.setItem(STATE_KEY, state);
        const params = new URLSearchParams({
            response_type: "code",
            client_id: config.clientId,
            redirect_uri: config.redirectUri,
            scope: config.scopes,
            code_challenge_method: "S256",
            code_challenge: await challenge(verifier),
            state,
        });
        window.location.assign(`${config.domain}/oauth2/authorize?${params}`);
    }

    async function exchangeCode() {
        const params = new URLSearchParams(window.location.search);
        if (params.get("error")) {
            clearCallbackParams();
            throw new Error("Sign in was cancelled or could not be completed.");
        }
        const code = params.get("code");
        if (!code) return false;
        if (params.get("state") !== sessionStorage.getItem(STATE_KEY)) {
            clearCallbackParams();
            throw new Error("Your sign-in session is invalid. Please try again.");
        }
        const verifier = sessionStorage.getItem(VERIFIER_KEY);
        if (!verifier) {
            clearCallbackParams();
            throw new Error("Your sign-in session expired. Please try again.");
        }
        const response = await fetch(`${config.domain}/oauth2/token`, {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: new URLSearchParams({
                grant_type: "authorization_code",
                client_id: config.clientId,
                code,
                redirect_uri: config.redirectUri,
                code_verifier: verifier,
            }),
        });
        if (!response.ok) {
            clearCallbackParams();
            throw new Error("We could not finish signing you in. Please try again.");
        }
        const tokens = await response.json();
        if (!tokens.access_token) {
            clearCallbackParams();
            throw new Error("No sign-in token was returned. Please try again.");
        }
        sessionStorage.setItem(TOKEN_KEY, tokens.access_token);
        sessionStorage.removeItem(STATE_KEY);
        sessionStorage.removeItem(VERIFIER_KEY);
        clearCallbackParams();
        return true;
    }

    function accessToken() {
        return sessionStorage.getItem(TOKEN_KEY);
    }

    function clearSession() {
        sessionStorage.removeItem(TOKEN_KEY);
    }

    function logout() {
        clearSession();
        if (config && config.domain && config.clientId) {
            const params = new URLSearchParams({
                client_id: config.clientId,
                logout_uri: config.logoutUri,
            });
            window.location.assign(`${config.domain}/logout?${params}`);
        } else {
            window.location.reload();
        }
    }

    return { loadConfig, login, exchangeCode, accessToken, clearSession, logout };
})();
