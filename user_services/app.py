from flask import Flask,request,jsonify,g,current_app
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy import text
import os
import requests
from common.auth import cognito_required
load_dotenv()
app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
db=SQLAlchemy(app)
class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    family_name=db.Column(db.String(100),nullable=True)
    email=db.Column(db.String(150),unique=True,nullable=False)
    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "family_name":self.family_name,
            "email":self.email
        }
    cognito_sub=db.Column(db.String(255),unique=True,index=True,nullable=True)
@app.route("/users", methods=["POST"])
@cognito_required
def create_user():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "JSON body required"
        }), 400

    name = data.get("name")
    email = data.get("email")

    if not name or not email:
        return jsonify({
            "error": "name and email are required"
        }), 400

    existing_user = User.query.filter_by(
        email=email
    ).first()

    if existing_user:
        return jsonify({
            "error": "Email already exists"
        }), 409

    user = User(
        name=name,
        email=email
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User created",
        "user": user.to_dict()
    }), 201
@app.route("/users", methods=["GET"])
def get_users():

    users = User.query.all()

    return jsonify([
        user.to_dict()
        for user in users
    ])
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):

    user = db.session.get(User, user_id)

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify(user.to_dict())
@app.route("/users/<int:user_id>", methods=["DELETE"])
@cognito_required
def delete_user(user_id):

    user = db.session.get(User, user_id)

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        "message": "User deleted"
    })

@app.route("/health")
def health():

    return jsonify({
        "service": "user-service",
        "status": "UP"
    })


with app.app_context():
    db.create_all()
    db.session.execute(text(
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS cognito_sub VARCHAR(255)"
    ))
    db.session.execute(text(
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS family_name VARCHAR(100)"
    ))
    db.session.execute(text(
        "CREATE UNIQUE INDEX IF NOT EXISTS ix_users_cognito_sub "
        "ON users (cognito_sub) WHERE cognito_sub IS NOT NULL"
    ))
    db.session.commit()
@app.route("/users/me", methods=["GET"])
@cognito_required
def get_current_user():
    claims = g.cognito_claims
    cognito_sub = claims["sub"]

    # ── Safe debug log (no token values) ─────────────────────────────────────
    current_app.logger.info(
        "[/users/me] sub_present=%s cognito_domain_configured=%s",
        bool(cognito_sub),
        bool(os.getenv("COGNITO_DOMAIN")),
    )

    cognito_domain = os.getenv("COGNITO_DOMAIN")
    if not cognito_domain:
        current_app.logger.error("[/users/me] COGNITO_DOMAIN is not set — cannot call UserInfo")
        return jsonify({
            "error": "Cognito profile verification is not configured",
            "reason": "cognito_configuration_missing",
        }), 503

    # ── Call Cognito UserInfo (best-effort) ───────────────────────────────────
    profile = {}
    profile_verified = False
    try:
        profile_response = requests.get(
            f"{cognito_domain.rstrip('/')}/oauth2/userInfo",
            headers={"Authorization": f"Bearer {g.cognito_access_token}"},
            timeout=5,
        )
        current_app.logger.info(
            "[/users/me] UserInfo status=%s", profile_response.status_code
        )
        if profile_response.status_code == 200:
            try:
                profile = profile_response.json()
                profile_verified = True
                current_app.logger.info(
                    "[/users/me] UserInfo claims present: %s",
                    sorted(profile.keys()),
                )
            except ValueError:
                current_app.logger.warning("[/users/me] UserInfo returned non-JSON body")
        else:
            current_app.logger.warning(
                "[/users/me] UserInfo rejected: status=%s body=%s",
                profile_response.status_code,
                profile_response.text[:200],
            )
    except requests.RequestException as exc:
        current_app.logger.warning("[/users/me] UserInfo request failed: %s", exc)

    current_app.logger.info(
        "[/users/me] email_present=%s given_name_present=%s family_name_present=%s "
        "email_verified=%s",
        bool(profile.get("email")),
        bool(profile.get("given_name")),
        bool(profile.get("family_name")),
        profile.get("email_verified"),
    )

    # ── Extract profile fields — all best-effort ─────────────────────────────
    email = (
        profile.get("email")
        or f"{cognito_sub}@cognito.local"
    )
    given_name = (
        profile.get("given_name")
        or profile.get("name")
        or email.split("@")[0]
    )
    family_name = profile.get("family_name") or ""
    name = f"{given_name} {family_name}".strip()

    # ── Sync local user record ────────────────────────────────────────────────
    user = User.query.filter_by(cognito_sub=cognito_sub).first()

    if not user:
        # Try to link by email if a legacy record exists
        user = User.query.filter_by(email=email).first()
        if user:
            user.cognito_sub = cognito_sub
            user.name = name
            if family_name:
                user.family_name = family_name
        else:
            user = User(
                name=name,
                family_name=family_name or None,
                email=email,
                cognito_sub=cognito_sub,
            )
            db.session.add(user)
    else:
        user.name = name
        if family_name:
            user.family_name = family_name
        user.email = email

    db.session.commit()

    result = user.to_dict()
    result["identity_provider"] = "Amazon Cognito User Pool"
    result["cognito_profile_verified"] = profile_verified
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)