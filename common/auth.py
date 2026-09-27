import os
from functools import wraps
from threading import Lock

import jwt
import requests
from flask import current_app, g, jsonify, request
from jwt import InvalidTokenError


_jwks_cache = None
_jwks_lock = Lock()


def _config():
    region = os.getenv("COGNITO_REGION")
    pool_id = os.getenv("COGNITO_USER_POOL_ID")
    issuer = os.getenv("COGNITO_ISSUER")
    if not issuer and region and pool_id:
        issuer = f"https://cognito-idp.{region}.amazonaws.com/{pool_id}"
    return issuer, os.getenv("COGNITO_CLIENT_ID")


def _jwks(issuer, force_refresh=False):
    global _jwks_cache
    if _jwks_cache and _jwks_cache["issuer"] == issuer and not force_refresh:
        return _jwks_cache["keys"]

    with _jwks_lock:
        if _jwks_cache and _jwks_cache["issuer"] == issuer and not force_refresh:
            return _jwks_cache["keys"]

        response = requests.get(f"{issuer}/.well-known/jwks.json", timeout=5)
        response.raise_for_status()
        keys = response.json()["keys"]
        _jwks_cache = {"issuer": issuer, "keys": keys}
        return keys


def validate_access_token(token):
    issuer, client_id = _config()
    import logging
    logging.getLogger(__name__).info(
        "[validate_access_token] issuer_configured=%s client_id_configured=%s",
        bool(issuer),
        bool(client_id),
    )
    if not issuer or not client_id:
        raise RuntimeError("Cognito authentication is not configured")

    try:
        header = jwt.get_unverified_header(token)
    except jwt.InvalidTokenError as error:
        raise InvalidTokenError("malformed_jwt") from error

    if header.get("alg") != "RS256" or not header.get("kid"):
        raise InvalidTokenError("unexpected_algorithm")

    key_data = next(
        (key for key in _jwks(issuer) if key.get("kid") == header["kid"]),
        None,
    )
    if not key_data:
        key_data = next(
            (key for key in _jwks(issuer, force_refresh=True) if key.get("kid") == header["kid"]),
            None,
        )
    if not key_data:
        raise InvalidTokenError("signing_key_not_found")

    signing_key = jwt.algorithms.RSAAlgorithm.from_jwk(key_data)
    claims = jwt.decode(
        token,
        signing_key,
        algorithms=["RS256"],
        issuer=issuer,
        options={
            "require": ["exp", "iss", "client_id", "token_use"],
            "verify_aud": False,
        },
    )
    if claims.get("token_use") != "access":
        raise InvalidTokenError("wrong_token_use")
    if claims.get("client_id") != client_id:
        raise InvalidTokenError("client_id_mismatch")
    if not claims.get("sub"):
        raise InvalidTokenError("missing_sub")
    return claims


def cognito_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        parts = auth_header.split()
        current_app.logger.info(
            "[cognito_required] path=%s authorization_header_present=%s",
            request.path,
            bool(auth_header),
        )
        if not auth_header:
            return _auth_rejection("missing_authorization", "Authorization header is required", 401)
        bearer_valid = len(parts) == 2 and parts[0].lower() == "bearer" and bool(parts[1])
        current_app.logger.info(
            "[cognito_required] bearer_format_valid=%s",
            bearer_valid,
        )
        if not bearer_valid:
            return _auth_rejection("malformed_bearer", "Use Authorization: Bearer <access token>", 401)
        try:
            g.cognito_access_token = parts[1]
            g.cognito_claims = validate_access_token(parts[1])
        except RuntimeError as error:
            return _auth_rejection("cognito_configuration_missing", str(error), 503)
        except jwt.ExpiredSignatureError:
            return _auth_rejection("token_expired", "Cognito access token has expired", 401)
        except jwt.InvalidIssuerError:
            return _auth_rejection("issuer_mismatch", "Cognito access token issuer does not match this service", 401)
        except jwt.InvalidSignatureError:
            return _auth_rejection("invalid_signature", "Cognito access token signature is invalid", 401)
        except InvalidTokenError as error:
            reason = str(error)
            if reason not in {
                "signing_key_not_found",
                "wrong_token_use",
                "client_id_mismatch",
                "missing_sub",
                "malformed_jwt",
                "unexpected_algorithm",
            }:
                reason = "invalid_token"
            messages = {
                "signing_key_not_found": "Cognito signing key was not found",
                "wrong_token_use": "Cognito access token required",
                "client_id_mismatch": "Access token belongs to a different Cognito App Client",
                "missing_sub": "Cognito token subject is missing",
                "malformed_jwt": "Cognito access token is malformed",
                "unexpected_algorithm": "Cognito token signing algorithm is invalid",
                "invalid_token": "Cognito access token is invalid",
            }
            return _auth_rejection(reason, messages[reason], 401)
        except requests.RequestException:
            return _auth_rejection("jwks_unavailable", "Cognito signing keys are temporarily unavailable", 503)
        except (ValueError, TypeError):
            return _auth_rejection("invalid_token", "Cognito access token is invalid", 401)
        current_app.logger.info(
            "[cognito_required] jwt_valid=True sub_present=%s token_use=%s client_id_matches=%s",
            bool(g.cognito_claims.get("sub")),
            g.cognito_claims.get("token_use"),
            g.cognito_claims.get("client_id") == os.getenv("COGNITO_CLIENT_ID"),
        )
        return function(*args, **kwargs)

    return decorated


def _auth_rejection(reason, message, status):
    current_app.logger.warning("Cognito authentication rejected: %s", reason)
    return jsonify({"error": message, "reason": reason}), status


def service_or_cognito_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        parts = auth_header.split()
        service_token = os.getenv("INTERNAL_SERVICE_TOKEN")
        if (
            service_token
            and len(parts) == 2
            and parts[0] == "Bearer"
            and parts[1] == service_token
        ):
            g.service_request = True
            return function(*args, **kwargs)
        return cognito_required(function)(*args, **kwargs)

    return decorated


def admin_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        # First ensure the user is authenticated via Cognito
        return cognito_required(_admin_check_logic(function))(*args, **kwargs)
    return decorated


def _admin_check_logic(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        groups = g.cognito_claims.get("cognito:groups", [])
        if not groups:
            groups = []
        is_admin = any(g.lower() in ["admin", "administrator", "admins"] for g in groups)
        
        # Fallback check for custom attribute if groups are not used
        custom_role = g.cognito_claims.get("custom:role", "")
        if custom_role and custom_role.lower() in ["admin", "administrator"]:
            is_admin = True
            
        if not is_admin:
            return _auth_rejection("insufficient_permissions", "Administrator access required", 403)
        return function(*args, **kwargs)
    return decorated