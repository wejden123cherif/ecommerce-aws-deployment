import os
from flask import Flask, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.jinja_env.globals["static_version"] = os.getenv("STATIC_VERSION", "2026-09-26")


@app.route("/")
def home():
    return render_template("index.html", static_version=app.jinja_env.globals["static_version"])


@app.route("/config")
def config():
    return jsonify({
        "domain": os.getenv("COGNITO_DOMAIN", ""),
        "clientId": os.getenv("COGNITO_CLIENT_ID", ""),
        "redirectUri": os.getenv("COGNITO_REDIRECT_URI", ""),
        "logoutUri": os.getenv("COGNITO_LOGOUT_URI", ""),
        "scopes": os.getenv("COGNITO_SCOPES", "openid email profile"),
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5500,
        debug=True
    )