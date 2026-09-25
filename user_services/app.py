from flask import Flask,request,jsonify,g
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from sqlalchemy import text
import os
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
    email=db.Column(db.String(150),unique=True,nullable=False)
    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
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
        "CREATE UNIQUE INDEX IF NOT EXISTS ix_users_cognito_sub "
        "ON users (cognito_sub) WHERE cognito_sub IS NOT NULL"
    ))
    db.session.commit()
@app.route("/users/me", methods=["GET"])
@cognito_required
def get_current_user():
    claims = g.cognito_claims
    cognito_sub = claims["sub"]
    user = User.query.filter_by(cognito_sub=cognito_sub).first()
    email = claims.get("email") or f"{cognito_sub}@cognito.local"
    name = claims.get("name") or claims.get("username") or email

    if not user:
        user = User.query.filter_by(email=email).first()
        if user:
            user.cognito_sub = cognito_sub
        else:
            user = User(name=name, email=email, cognito_sub=cognito_sub)
            db.session.add(user)
        db.session.commit()

    return jsonify(user.to_dict())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)