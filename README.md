# E-Commerce Microservices

A complete **E-Commerce Microservices application** built using **Python, Flask, PostgreSQL, REST APIs, API Gateway, and a web frontend**.

The project demonstrates how independent microservices communicate with each other and how an API Gateway provides a single entry point for clients.

---

## 🚀 Features

* User Microservice
* Product Microservice
* Order Microservice
* API Gateway
* PostgreSQL database
* RESTful APIs
* Amazon Cognito authentication with Authorization Code + PKCE
* Product stock management
* Order creation and validation
* Microservice-to-microservice communication
* Frontend dashboard
* CORS support
* Environment-based configuration
* Git/GitHub ready

---

## 🏗️ Architecture

```text
                         Browser
                            |
                            v
                    Frontend :5500
                            |
                            v
                  API Gateway :5000
                     /      |      \
                    /       |       \
                   v        v        v
             User :5002  Product :5001  Order :5003
                 |           |            |
                 v           v            v
             PostgreSQL  PostgreSQL   PostgreSQL
```

### Order Flow

```text
Client
  |
  v
API Gateway
  |
  v
Order Service
  |
  +----> User Service
  |          |
  |          v
  |      Verify User
  |
  +----> Product Service
             |
             v
         Verify Product
             |
             v
         Check Stock
             |
             v
        Reduce Stock
             |
             v
        Create Order
```

---

## 🛠️ Technologies

### Backend

* Python
* Flask
* Flask-SQLAlchemy
* REST API
* Requests

### Database

* PostgreSQL
* SQLAlchemy ORM

### Authentication

* Verified Cognito access tokens

### Frontend

* HTML
* CSS
* JavaScript
* Flask

### Development Tools

* Git
* GitHub
* PowerShell
* VS Code

---

## 📁 Project Structure

```text
ecommerce-microservices/
│
├── api_gateway/
│   ├── app.py
│   └── .env
│
├── user_services/
│   ├── app.py
│   └── .env
│
├── product_services/
│   ├── app.py
│   └── .env
│
├── order_service/
│   ├── app.py
│   └── .env
│
├── front_end/
│   ├── app.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── app.js
│       └── styles.css
│
├── .gitignore
├── README.md
└── requirements.txt
```

> `.env` files contain secrets and should not be committed to GitHub.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/ecommerce-microservices.git
```

```bash
cd ecommerce-microservices
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available:

```bash
pip install Flask Flask-SQLAlchemy psycopg2-binary python-dotenv requests flask-cors
```

---

## 🗄️ PostgreSQL Setup

Create the required PostgreSQL databases:

```sql
CREATE DATABASE ecommerce_user_db;

CREATE DATABASE ecommerce_product_db;

CREATE DATABASE ecommerce_order_db;
```

Configure each service's `.env` file.

Example:

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ecommerce_user_db
COGNITO_REGION=your-region
COGNITO_USER_POOL_ID=your-user-pool-id
COGNITO_CLIENT_ID=your-public-app-client-id
```

Use the appropriate database name for each service.

### Product Service

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ecommerce_product_db
COGNITO_REGION=your-region
COGNITO_USER_POOL_ID=your-user-pool-id
COGNITO_CLIENT_ID=your-public-app-client-id
```

### User Service

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ecommerce_user_db
COGNITO_REGION=your-region
COGNITO_USER_POOL_ID=your-user-pool-id
COGNITO_CLIENT_ID=your-public-app-client-id
```

### Order Service

```env
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/ecommerce_order_db
COGNITO_REGION=your-region
COGNITO_USER_POOL_ID=your-user-pool-id
COGNITO_CLIENT_ID=your-public-app-client-id
INTERNAL_SERVICE_TOKEN=server-only-placeholder

USER_SERVICE_URL=http://localhost:5002
PRODUCT_SERVICE_URL=http://localhost:5001
```

> Never commit real passwords, tokens, or Cognito values to GitHub.

---

## ▶️ Running the Application

Start each service in a separate terminal.

### Product Service

```bash
cd product_services
python app.py
```

Runs on:

```text
http://localhost:5001
```

### User Service

```bash
cd user_services
python app.py
```

Runs on:

```text
http://localhost:5002
```

### Order Service

```bash
cd order_service
python app.py
```

Runs on:

```text
http://localhost:5003
```

### API Gateway

```bash
cd api_gateway
python app.py
```

Runs on:

```text
http://localhost:5000
```

### Frontend

```bash
cd front_end
python app.py
```

Runs on:

```text
http://localhost:5500
```

---

# 🔌 API Endpoints

## Users

### Create User

```http
POST /users
```

Example request:

```json
{
    "name": "Raj",
    "email": "raj@gmail.com"
}
```

### Get Users

```http
GET /users
```

### Get User

```http
GET /users/{id}
```

---

## Products

### Create Product

```http
POST /products
```

Example:

```json
{
    "name": "Laptop",
    "price": 55000,
    "stock": 10
}
```

### Get Products

```http
GET /products
```

### Get Product

```http
GET /products/{id}
```

### Update Stock

```http
PUT /products/{id}/stock
```

Example:

```json
{
    "stock": 20
}
```

### Delete Product

```http
DELETE /products/{id}
```

---

## Orders

### Create Order

```http
POST /orders
```

Example:

```json
{
    "user_id": 1,
    "product_id": 1,
    "quantity": 2
}
```

### Get Orders

```http
GET /orders
```

### Get Order

```http
GET /orders/{id}
```

---

# 🧪 Example API Flow

### 1. Create User

```text
POST /users
```

```json
{
    "name": "Raj",
    "email": "raj@gmail.com"
}
```

User ID:

```text
1
```

### 2. Create Product

```text
POST /products
```

```json
{
    "name": "Laptop",
    "price": 55000,
    "stock": 10
}
```

Product ID:

```text
1
```

### 3. Create Order

```text
POST /orders
```

```json
{
    "user_id": 1,
    "product_id": 1,
    "quantity": 2
}
```

The system:

1. Checks whether the user exists.
2. Checks whether the product exists.
3. Checks product stock.
4. Calculates total price.
5. Reduces product stock.
6. Creates the order.
7. Stores the order in PostgreSQL.

Example:

```text
Product price = ₹55,000
Quantity      = 2

Total         = ₹110,000
```

Stock:

```text
Before order = 10
Quantity     = 2
After order  = 8
```

---

# 🌐 Frontend

The frontend dashboard is available at:

```text
http://localhost:5500
```

It displays:

* Users
* Products
* Product stock
* Orders
* Order quantity
* Order total
* Order status

---

# 🔒 Security

Protected API requests use a verified Cognito access token. The browser never receives the server-only `INTERNAL_SERVICE_TOKEN`.

---

# 📊 Example Result

```text
E-Commerce Dashboard

Users
-------------------------
Raj
ID: 1
Email: raj@gmail.com

Products
-------------------------
Laptop
Price: ₹55,000
Stock: 8

Orders
-------------------------
Order #1
User ID: 1
Product ID: 1
Quantity: 2
Total: ₹110,000
Status: CONFIRMED
```

---

# 🚀 Future Improvements

* Docker and Docker Compose
* JWT authentication
* Redis caching
* RabbitMQ/Kafka messaging
* API documentation with Swagger/OpenAPI
* Unit and integration tests
* CI/CD with GitHub Actions
* Centralized logging
* Monitoring and health checks
* Kubernetes deployment
* Payment service
* Inventory service
* Notification service

## Authentication

The browser uses an Amazon Cognito User Pool public App Client with OAuth 2.0 Authorization Code Flow and PKCE. Cognito Managed Login collects and verifies the user's email, given name, and family name according to the User Pool attribute settings. The app stores the short-lived access token in `sessionStorage`; it does not use an ID token or refresh token as API authorization, and it never contains a client secret.

The frontend reads these placeholders from its environment:

```env
COGNITO_DOMAIN=https://your-domain.auth.your-region.amazoncognito.com
COGNITO_CLIENT_ID=your-public-app-client-id
COGNITO_REDIRECT_URI=http://localhost:5500/
COGNITO_LOGOUT_URI=http://localhost:5500/
COGNITO_SCOPES=openid email profile
```

The API Gateway, user service, order service, and product service validate access-token signatures using the Cognito JWKS endpoint. They check the issuer, expiration, `RS256`, `token_use=access`, `sub`, and the expected `client_id`. JWKS keys are cached in memory. The user service then calls Cognito UserInfo with that already-validated access token and uses the returned `email`, `given_name`, and `family_name` claims for profile synchronization.

`GET /users/me` maps the verified Cognito `sub` to `users.cognito_sub`, synchronizing the email, given name, and family name profile on first access. It reports the identity provider as Amazon Cognito only after the verified UserInfo lookup succeeds. The `cognito_sub` column is nullable so existing users are preserved. The order service derives `orders.user_id` from this mapping, filters `GET /orders` to that user, and returns 404 for another user's order. A conflicting body `user_id` on `POST /orders` is rejected.

### AWS Cognito configuration required after this code change

Create a User Pool, a public App Client with no client secret, a hosted UI domain, and callback/logout URLs matching the configured values. Enable email sign-up and verification. Add `email`, `given_name`, and `family_name` as required or writable standard attributes according to your registration policy. Allow the `openid`, `email`, and `profile` scopes so Cognito UserInfo can return the profile. Then provide these values to Compose as placeholders replaced by your deployment configuration:

```env
COGNITO_REGION=your-region
COGNITO_USER_POOL_ID=your-user-pool-id
COGNITO_CLIENT_ID=your-public-app-client-id
COGNITO_ISSUER=https://cognito-idp.your-region.amazonaws.com/your-user-pool-id
COGNITO_DOMAIN=https://your-domain.auth.your-region.amazoncognito.com
COGNITO_REDIRECT_URI=https://your-frontend-host/
COGNITO_LOGOUT_URI=https://your-frontend-host/
COGNITO_SCOPES=openid email profile
INTERNAL_SERVICE_TOKEN=server-only-internal-placeholder
```

### Database migration

On startup, the user service runs an additive PostgreSQL migration equivalent to:

```sql
ALTER TABLE users ADD COLUMN IF NOT EXISTS cognito_sub VARCHAR(255);
CREATE UNIQUE INDEX IF NOT EXISTS ix_users_cognito_sub
ON users (cognito_sub) WHERE cognito_sub IS NOT NULL;
```

It does not drop tables, delete users, or wipe existing data.

---

# 👨‍💻 Author

**Raj**

Python | Flask | PostgreSQL | REST API | Microservices

---

## 📄 License

This project is created for learning and portfolio purposes.

