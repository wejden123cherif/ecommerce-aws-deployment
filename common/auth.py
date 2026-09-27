import os
from functools import wraps
from threading import Lock

import jwt
import requests
from flask import g, jsonify, request
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
    if not issuer or not client_id:
        raise RuntimeError("Cognito authentication is not configured")

    try:
        header = jwt.get_unverified_header(token)
    except jwt.InvalidTokenError as error:
        raise InvalidTokenError("Malformed JWT") from error

    if header.get("alg") != "RS256" or not header.get("kid"):
        raise InvalidTokenError("Unexpected signing algorithm")

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
        raise InvalidTokenError("Signing key not found")

    signing_key = jwt.algorithms.RSAAlgorithm.from_jwk(key_data)
    claims = jwt.decode(
        token,
        signing_key,
        algorithms=["RS256"],
        issuer=issuer,
        options={
            "require": ["exp", "iss", "sub", "client_id", "token_use"],
            "verify_aud": False,
        },
    )
    if claims.get("token_use") != "access":
        raise InvalidTokenError("Access token required")
    if claims.get("client_id") != client_id:
        raise InvalidTokenError("Unexpected Cognito client")
    if not claims.get("sub"):
        raise InvalidTokenError("Token subject is required")
    return claims


def cognito_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        parts = auth_header.split()
        if len(parts) != 2 or parts[0] != "Bearer" or not parts[1]:
            return jsonify({"error": "Valid Bearer access token required"}), 401
        try:
            g.cognito_access_token = parts[1]
            g.cognito_claims = validate_access_token(parts[1])
        except RuntimeError as error:
            return jsonify({"error": str(error)}), 503
        except jwt.ExpiredSignatureError:
            return jsonify({
                "error": "Cognito access token has expired",
                "reason": "token_expired",
            }), 401
        except jwt.InvalidIssuerError:
            return jsonify({
                "error": "Cognito access token issuer does not match this service",
                "reason": "issuer_mismatch",
            }), 401
        except jwt.InvalidSignatureError:
            return jsonify({
                "error": "Cognito access token signature is invalid",
                "reason": "invalid_signature",
            }), 401
        except InvalidTokenError as error:
            if str(error) == "Unexpected Cognito client":
                return jsonify({
                    "error": "Access token belongs to a different Cognito App Client",
                    "reason": "client_id_mismatch",
                }), 401
            if str(error) == "Access token required":
                return jsonify({
                    "error": "Cognito access token required",
                    "reason": "wrong_token_use",
                }), 401
            return jsonify({
                "error": "Cognito access token is invalid",
                "reason": "invalid_token",
            }), 401
        except requests.RequestException:
            return jsonify({
                "error": "Cognito signing keys are temporarily unavailable",
                "reason": "jwks_unavailable",
            }), 503
        except (ValueError, TypeError):
            return jsonify({
                "error": "Cognito access token is invalid",
                "reason": "invalid_token",
            }), 401
        return function(*args, **kwargs)

    return decorated


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