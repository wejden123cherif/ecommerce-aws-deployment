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

    function validateConfigValues() {
        const required = [
            ["domain", "COGNITO_DOMAIN"],
            ["clientId", "COGNITO_CLIENT_ID"],
            ["redirectUri", "COGNITO_REDIRECT_URI"],
            ["logoutUri", "COGNITO_LOGOUT_URI"],
            ["scopes", "COGNITO_SCOPES"],
        ];

        const missing = required.filter(([, envName]) => {
            const value = config?.[envName.replace("COGNITO_", "").replace("_", "")];
            return !value;
        });

        if (missing.length) {
            const names = missing.map(([key, envKey]) => envKey).join(", ");
            throw new Error(
                `Cognito configuration is incomplete. Set ${names} before starting sign in.`
            );
        }
    }

    function clearCallbackParams() {
        window.history.replaceState({}, document.title, window.location.pathname);
    }

    async function loadConfig() {
        const response = await fetch("/config");
        if (!response.ok) {
            console.warn("Cognito configuration request failed", { status: response.status });
            throw new Error("Authentication settings are unavailable.");
        }
        config = await response.json();
        console.log("Cognito config:", {
            domain: config.domain,
            clientId: config.clientId,
            redirectUri: config.redirectUri,
            logoutUri: config.logoutUri,
            scopes: config.scopes,
        });
        const required = ["domain", "clientId", "redirectUri", "logoutUri", "scopes"];
        const missing = required.filter((key) => !config[key]);
        if (missing.length) {
            throw new Error(
                `Cognito configuration is incomplete. Missing: ${missing.join(", ")}.`
            );
        }
        return config;
    }

    async function login() {
        if (!config) await loadConfig();

        const required = ["domain", "clientId", "redirectUri", "logoutUri", "scopes"];
        const missing = required.filter((key) => !config[key]);
        if (missing.length) {
            throw new Error(
                `Secure sign-in is not configured. Missing ${missing.join(", ")}.`
            );
        }

        const verifier = randomString();
        const state = randomString();
        sessionStorage.setItem(VERIFIER_KEY, verifier);
        sessionStorage.setItem(STATE_KEY, state);

        const challengeValue = await challenge(verifier);
        const authorizeUrl = new URL("/oauth2/authorize", config.domain);
        authorizeUrl.searchParams.set("response_type", "code");
        authorizeUrl.searchParams.set("client_id", config.clientId);
        authorizeUrl.searchParams.set("redirect_uri", config.redirectUri);
        authorizeUrl.searchParams.set("scope", config.scopes);
        authorizeUrl.searchParams.set("state", state);
        authorizeUrl.searchParams.set("code_challenge", challengeValue);
        authorizeUrl.searchParams.set("code_challenge_method", "S256");

        console.log("Authorization URL:", authorizeUrl.toString());
        window.location.assign(authorizeUrl.toString());
    }

    async function exchangeCode() {
        const params = new URLSearchParams(window.location.search);
        if (params.get("error")) {
            const error = params.get("error");
            const errorDescription = params.get("error_description") || "No description provided";
            console.error("Cognito authentication error:", {
                error,
                error_description: errorDescription,
            });
            clearCallbackParams();
            throw new Error(callbackErrorMessage(error, errorDescription));
        }
        const code = params.get("code");
        if (!code) return false;
        if (params.get("state") !== sessionStorage.getItem(STATE_KEY)) {
            console.warn("Cognito callback state mismatch");
            sessionStorage.removeItem(STATE_KEY);
            sessionStorage.removeItem(VERIFIER_KEY);
            clearCallbackParams();
            throw new Error("Your sign-in session is invalid. Please try again.");
        }
        const verifier = sessionStorage.getItem(VERIFIER_KEY);
        if (!verifier) {
            console.warn("Cognito callback PKCE verifier is missing");
            sessionStorage.removeItem(STATE_KEY);
            clearCallbackParams();
            throw new Error("Your sign-in session expired. Please try again.");
        }

        const tokenUrl = new URL("/oauth2/token", config.domain);
        const response = await fetch(tokenUrl.toString(), {
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
            console.warn("Cognito token exchange failed", {
                status: response.status,
                error: await safeErrorResponse(response),
            });
            clearCallbackParams();
            throw new Error("Cognito could not complete sign in. Check the callback URL, client, scopes, and PKCE settings.");
        }
        const tokens = await response.json();
        if (!tokens.access_token) {
            console.warn("Cognito token response did not contain an access token");
            clearCallbackParams();
            throw new Error("No sign-in token was returned. Please try again.");
        }
        sessionStorage.setItem(TOKEN_KEY, tokens.access_token);
        sessionStorage.removeItem(STATE_KEY);
        sessionStorage.removeItem(VERIFIER_KEY);
        clearCallbackParams();
        return true;
    }

    function callbackErrorMessage(error, description = "") {
        if (error === "access_denied") return "Sign in was cancelled.";
        if (description.includes("invalid_scope")) {
            return "Cognito rejected the requested scope. Enable openid, email, and profile for this App Client.";
        }
        if (error === "invalid_request") return "Cognito rejected the sign-in request. Check the callback URL and client settings.";
        return "Cognito could not complete sign in. Please try again.";
    }

    async function safeErrorResponse(response) {
        try {
            const body = await response.clone().json();
            return { error: body.error, description: body.error_description };
        } catch (error) {
            return { statusText: response.statusText };
        }
    }

    function accessToken() {
        return sessionStorage.getItem(TOKEN_KEY);
    }

    function clearSession() {
        sessionStorage.removeItem(TOKEN_KEY);
        sessionStorage.removeItem(STATE_KEY);
        sessionStorage.removeItem(VERIFIER_KEY);
    }

    function logout() {
        clearSession();
        if (config && config.domain && config.clientId && config.logoutUri) {
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
