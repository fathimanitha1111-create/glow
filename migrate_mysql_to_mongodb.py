"""
Migration Script: Import existing MySQL data into MongoDB.
Reads from mysql_data_backup.json (generated from MySQL simple_db)
and safely creates all Categories, Products, Users, Orders, and OrderItems
in the local MongoDB database without data loss.
"""

import os
import sys
import json
from decimal import Decimal
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple.settings')

import django
django.setup()

from django.contrib.auth.models import User
from simpleapp.models import Category, Product, Order, OrderItem

def migrate():
    backup_path = BASE_DIR / 'mysql_data_backup.json'
    if not backup_path.exists():
        print(f"[-] Backup file not found at: {backup_path}")
        print("    Running seed_data.py instead...")
        import seed_data
        seed_data.seed()
        return

    with open(backup_path, 'r', encoding='utf-8') as f:
        backup = json.load(f)

    print("=" * 65)
    print("[*] GLOW & CARE - MIGRATING MYSQL BACKUP TO MONGODB")
    print("=" * 65)

    # 1. Categories
    print("\n[*] Migrating Categories...")
    category_map = {} # old_id -> new Category instance
    for row in backup.get('simpleapp_category', []):
        old_id = row['id']
        cat, created = Category.objects.get_or_create(
            slug=row['slug'],
            defaults={
                'name': row['name'],
                'description': row.get('description', ''),
                'image_url': row.get('image_url', ''),
            }
        )
        category_map[old_id] = cat
        print(f"  [Category] {cat.name} ({'Created' if created else 'Already exists'})")

    # 2. Products
    print("\n[*] Migrating Products...")
    product_map = {} # old_id -> new Product instance
    for row in backup.get('simpleapp_product', []):
        old_id = row['id']
        cat = category_map.get(row.get('category_id'))
        if not cat:
            cat = Category.objects.first()

        prod, created = Product.objects.get_or_create(
            name=row['name'],
            defaults={
                'category': cat,
                'description': row.get('description', ''),
                'ingredients': row.get('ingredients', ''),
                'skin_type': row.get('skin_type', 'sensitive'),
                'badge': row.get('badge', ''),
                'price': Decimal(str(row.get('price', '0.00'))),
                'original_price': Decimal(str(row['original_price'])) if row.get('original_price') else None,
                'stock': int(row.get('stock', 25)),
                'rating': Decimal(str(row.get('rating', '4.9'))),
                'review_count': int(row.get('review_count', 100)),
                'image_url': row.get('image_url', ''),
            }
        )
        product_map[old_id] = prod
        print(f"  [Product] {prod.name} (PK: {prod.pk})")

    # 3. Users
    print("\n[*] Migrating Users...")
    user_map = {} # old_id -> new User instance
    for row in backup.get('auth_user', []):
        old_id = row['id']
        u, created = User.objects.get_or_create(
            username=row['username'],
            defaults={
                'email': row.get('email', ''),
                'first_name': row.get('first_name', ''),
                'last_name': row.get('last_name', ''),
                'is_active': bool(row.get('is_active', True)),
                'is_staff': bool(row.get('is_staff', False)),
                'is_superuser': bool(row.get('is_superuser', False)),
            }
        )
        if created and 'password' in row:
            u.password = row['password']
            u.save()
        user_map[old_id] = u
        print(f"  [User] {u.username}")

    # 4. Orders & OrderItems
    print("\n[*] Migrating Orders and Items...")
    order_map = {}
    for row in backup.get('simpleapp_order', []):
        old_id = row['id']
        u = user_map.get(row.get('user_id'))
        order = Order.objects.create(
            user=u,
            full_name=row['full_name'],
            email=row['email'],
            phone=row['phone'],
            address=row['address'],
            city=row['city'],
            postal_code=row['postal_code'],
            total_amount=Decimal(str(row['total_amount'])),
            status=row.get('status', 'Confirmed'),
        )
        order_map[old_id] = order
        print(f"  [Order] Created Order #{order.id} for {order.full_name} (Total: ₹{order.total_amount})")

    for row in backup.get('simpleapp_orderitem', []):
        order = order_map.get(row.get('order_id'))
        prod = product_map.get(row.get('product_id'))
        if order and prod:
            item = OrderItem.objects.create(
                order=order,
                product=prod,
                price=Decimal(str(row['price'])),
                quantity=int(row['quantity']),
            )
            print(f"    [Item] {item.quantity}x {prod.name} -> Order #{order.id}")

    print("\n[+] MIGRATION TO MONGODB FINISHED SUCCESSFULLY!")
    print(f"    Total Categories: {Category.objects.count()}")
    print(f"    Total Products:   {Product.objects.count()}")
    print(f"    Total Orders:     {Order.objects.count()}")

if __name__ == '__main__':
    migrate()
