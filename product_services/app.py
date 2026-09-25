from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from common.auth import service_or_cognito_required

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)



# =========================
# PRODUCT MODEL
# =========================

class Product(db.Model):

    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "price": float(self.price),
            "stock": self.stock
        }


# =========================
# CREATE PRODUCT
# =========================

@app.route("/products", methods=["POST"])
@service_or_cognito_required
def create_product():

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "JSON body required"
        }), 400

    name = data.get("name")
    price = data.get("price")
    stock = data.get("stock")

    if not name or price is None or stock is None:

        return jsonify({
            "error": "name, price and stock are required"
        }), 400

    if price < 0:

        return jsonify({
            "error": "Price cannot be negative"
        }), 400

    if stock < 0:

        return jsonify({
            "error": "Stock cannot be negative"
        }), 400

    product = Product(
        name=name,
        price=price,
        stock=stock
    )

    db.session.add(product)
    db.session.commit()

    return jsonify({
        "message": "Product created successfully",
        "product": product.to_dict()
    }), 201


# =========================
# GET ALL PRODUCTS
# =========================

@app.route("/products", methods=["GET"])
def get_products():

    products = Product.query.all()

    return jsonify([
        product.to_dict()
        for product in products
    ]), 200


# =========================
# GET PRODUCT BY ID
# =========================

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):

    product = db.session.get(Product, product_id)

    if not product:

        return jsonify({
            "error": "Product not found"
        }), 404

    return jsonify(product.to_dict()), 200


# =========================
# UPDATE STOCK
# =========================

@app.route(
    "/products/<int:product_id>/stock",
    methods=["PUT"]
)
@service_or_cognito_required
def update_stock(product_id):

    product = db.session.get(Product, product_id)

    if not product:

        return jsonify({
            "error": "Product not found"
        }), 404

    data = request.get_json()

    if not data or "stock" not in data:

        return jsonify({
            "error": "stock is required"
        }), 400

    stock = data["stock"]

    if stock < 0:

        return jsonify({
            "error": "Stock cannot be negative"
        }), 400

    product.stock = stock

    db.session.commit()

    return jsonify({
        "message": "Stock updated successfully",
        "product": product.to_dict()
    }), 200


# =========================
# DELETE PRODUCT
# =========================

@app.route(
    "/products/<int:product_id>",
    methods=["DELETE"]
)
@service_or_cognito_required
def delete_product(product_id):

    product = db.session.get(Product, product_id)

    if not product:

        return jsonify({
            "error": "Product not found"
        }), 404

    db.session.delete(product)
    db.session.commit()

    return jsonify({
        "message": "Product deleted successfully"
    }), 200


# =========================
# HEALTH CHECK
# =========================

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "service": "product-service",
        "status": "UP"
    }), 200


# =========================
# CREATE TABLES
# =========================

with app.app_context():

    db.create_all()


# =========================
# RUN APPLICATION
# =========================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )