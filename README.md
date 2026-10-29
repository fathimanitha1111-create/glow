# glowithnitha — Glow & Care Skincare E-Commerce Platform

A clean, responsive, full-stack skincare e-commerce website built with **Django 5.2 (LTS)** and **MongoDB** (local database engine).

---

## Architecture & Technology Stack

- **Backend**: Django 5.2 (Python 3.12)
- **Database**: Local MongoDB Community Server (Port `27017`)
- **MongoDB Driver & Backend**: `django-mongodb-backend 5.2.4` + `pymongo 4.19`
- **Primary Keys**: BSON `ObjectId` via `ObjectIdAutoField`
- **Static Assets**: WhiteNoise + Bootstrap 5 + Custom Vanilla CSS
- **Features**: Product Catalog, Live Filter/Search, Dynamic Session Cart, Quantity Updates, Checkout, Order Tracking, Admin CRUD.

---

## Quickstart Guide (Windows PowerShell)

### 1. Install Python Dependencies
```powershell
py -m pip install -r requirements.txt
```

### 2. Start Local MongoDB Server
The MongoDB binaries and data directory are located in `C:\Users\LENOVO\mongodb`.

Start MongoDB using PowerShell:
```powershell
& "C:\Users\LENOVO\mongodb\bin\mongod.exe" --dbpath "C:\Users\LENOVO\mongodb\data" --port 27017 --bind_ip 127.0.0.1
```
*(Leave this terminal window open while working, or run in the background)*

### 3. Initialize Database & Run Migrations
Run the automated initialization script:
```powershell
py setup_db.py
```
Or manually run:
```powershell
py manage.py migrate
py migrate_mysql_to_mongodb.py
```

### 4. Run the Development Server
```powershell
py manage.py runserver
```
Visit the website in your browser at:
👉 **http://127.0.0.1:8000/**

---

## Verifying All Features (Automated Test Suite)

Run the included automated end-to-end test script:
```powershell
py test_mongodb_site.py
```
This tests all 11 core user flows:
1. Homepage & Bestseller rendering
2. Shop catalog
3. Keyword search
4. Category filtering
5. Product detail view
6. Add to cart
7. Cart subtotal and free shipping calculation
8. Cart quantity adjustment
9. Checkout & MongoDB Order document creation
10. Order success confirmation page
11. Session cleanup

---

## Environment Configuration (`.env`)

```ini
# Local MongoDB Database Settings
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_DB_NAME=simple_db
MONGO_USER=
MONGO_PASSWORD=
MONGO_URI=mongodb://localhost:27017/

# Django Core Settings
SECRET_KEY=django-insecure-simple-glow-skincare-secret-key-2026-xyz
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```
# glowithnitha
