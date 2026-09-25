import os
from flask import Flask, jsonify, render_template
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/config")
def config():
    return jsonify({
        "domain": os.getenv("COGNITO_DOMAIN", ""),
        "clientId": os.getenv("COGNITO_CLIENT_ID", ""),
        "redirectUri": os.getenv("COGNITO_REDIRECT_URI", "http://localhost:5500/"),
        "logoutUri": os.getenv("COGNITO_LOGOUT_URI", "http://localhost:5500/"),
        "scopes": os.getenv("COGNITO_SCOPES", "openid email profile"),
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5500,
        debug=True
    )