from flask import Flask,request,jsonify,g
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
    cognito_domain = os.getenv("COGNITO_DOMAIN")
    if not cognito_domain:
        return jsonify({"error": "Cognito profile verification is not configured"}), 503
    try:
        profile_response = requests.get(
            f"{cognito_domain.rstrip('/')}/oauth2/userInfo",
            headers={"Authorization": f"Bearer {g.cognito_access_token}"},
            timeout=5,
        )
        if profile_response.status_code != 200:
            return jsonify({"error": "Unable to verify Cognito profile"}), 401
        profile = profile_response.json()
    except requests.RequestException:
        return jsonify({"error": "Cognito profile service unavailable"}), 503

    required_profile = ("email", "given_name", "family_name")
    if (
        any(not profile.get(attribute) for attribute in required_profile)
        or profile.get("email_verified") is not True
    ):
        return jsonify({
            "error": "Cognito profile requires verified email, given name, and family name"
        }), 422
    cognito_sub = claims["sub"]
    user = User.query.filter_by(cognito_sub=cognito_sub).first()
    email = profile.get("email") or f"{cognito_sub}@cognito.local"
    given_name = profile.get("given_name") or profile.get("name") or profile.get("username") or email
    family_name = profile.get("family_name") or ""
    name = f"{given_name} {family_name}".strip()

    if not user:
        user = User.query.filter_by(email=email).first()
        if user:
            user.cognito_sub = cognito_sub
            user.name = name
            user.family_name = family_name or user.family_name
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
        user.family_name = family_name or user.family_name
        user.email = email

    db.session.commit()

    result = user.to_dict()
    result["identity_provider"] = "Amazon Cognito User Pool"
    result["cognito_profile_verified"] = True
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)