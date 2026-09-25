from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import requests
import os

from common.auth import cognito_required

load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

INTERNAL_SERVICE_TOKEN = os.getenv("INTERNAL_SERVICE_TOKEN")
USER_SERVICE_URL = os.getenv("USER_SERVICE_URL")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL")


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="CONFIRMED")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "total_price": float(self.total_price),
            "status": self.status,
        }


def current_user():
    try:
        response = requests.get(
            f"{USER_SERVICE_URL}/users/me",
            headers={"Authorization": request.headers.get("Authorization")},
            timeout=5,
        )
    except requests.RequestException:
        return None, (jsonify({"error": "User service unavailable"}), 503)
    if response.status_code != 200:
        return None, (jsonify({"error": "Unable to provision authenticated user"}), 503)
    return response.json(), None


@app.route("/orders", methods=["POST"])
@cognito_required
def create_order():
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    product_id = data.get("product_id")
    quantity = data.get("quantity")
    if not product_id or not quantity:
        return jsonify({"error": "product_id and quantity are required"}), 400
    if not isinstance(quantity, int) or quantity <= 0:
        return jsonify({"error": "Quantity must be greater than 0"}), 400

    user, error = current_user()
    if error:
        return error
    supplied_user_id = data.get("user_id")
    if supplied_user_id is not None and supplied_user_id != user["id"]:
        return jsonify({"error": "user_id must match the authenticated user"}), 403

    try:
        product_response = requests.get(
            f"{PRODUCT_SERVICE_URL}/products/{product_id}", timeout=5
        )
    except requests.RequestException:
        return jsonify({"error": "Product service unavailable"}), 503
    if product_response.status_code == 404:
        return jsonify({"error": "Product does not exist"}), 404
    if product_response.status_code != 200:
        return jsonify({"error": "Unable to validate product"}), 503

    product = product_response.json()
    if product["stock"] < quantity:
        return jsonify({
            "error": "Insufficient stock",
            "available_stock": product["stock"],
        }), 400

    try:
        stock_response = requests.put(
            f"{PRODUCT_SERVICE_URL}/products/{product_id}/stock",
            headers={"Authorization": f"Bearer {INTERNAL_SERVICE_TOKEN}"},
            json={"stock": product["stock"] - quantity},
            timeout=5,
        )
    except requests.RequestException:
        return jsonify({"error": "Unable to update product stock"}), 503
    if stock_response.status_code != 200:
        return jsonify({"error": "Stock update failed"}), 500

    order = Order(
        user_id=user["id"],
        product_id=product_id,
        quantity=quantity,
        total_price=product["price"] * quantity,
        status="CONFIRMED",
    )
    db.session.add(order)
    db.session.commit()
    return jsonify({
        "message": "Order created successfully",
        "order": order.to_dict(),
    }), 201


@app.route("/orders", methods=["GET"])
@cognito_required
def get_orders():
    user, error = current_user()
    if error:
        return error
    orders = Order.query.filter_by(user_id=user["id"]).all()
    return jsonify([order.to_dict() for order in orders])


@app.route("/orders/<int:order_id>", methods=["GET"])
@cognito_required
def get_order(order_id):
    user, error = current_user()
    if error:
        return error
    order = Order.query.filter_by(id=order_id, user_id=user["id"]).first()
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order.to_dict())


@app.route("/health")
def health():
    return jsonify({"service": "order-service", "status": "UP"})


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
