"""
Comprehensive Test Script for Glow & Care Skincare with MongoDB.
Tests all required views: Home, Shop, Category, Detail, Cart, Update Cart, Checkout, Order Success.
"""

import os
import sys

# Ensure UTF-8 output on Windows consoles
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple.settings')

import django
django.setup()

from django.test.utils import setup_test_environment
setup_test_environment()

from django.test import Client
from simpleapp.models import Category, Product, Order, OrderItem

def run_tests():
    print("=" * 65)
    print("[*] TESTING GLOW & CARE WEBSITE FUNCTIONALITY WITH MONGODB")
    print("=" * 65)

    client = Client()

    # 1. Test Home page
    print("\n1. Testing Home page (GET /)...")
    res = client.get('/')
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert len(res.context['bestsellers']) > 0, "No bestsellers in context"
    assert len(res.context['categories']) > 0, "No categories in context"
    print("   [+] PASS: Home page loaded with bestsellers and categories.")

    # 2. Test Shop page
    print("\n2. Testing Shop page (GET /shop/)...")
    res = client.get('/shop/')
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    product_count = len(res.context['products'])
    assert product_count == 12, f"Expected 12 products, got {product_count}"
    print(f"   [+] PASS: Shop page loaded with all {product_count} products.")

    # 3. Test Product Search
    print("\n3. Testing Product Search (GET /shop/?q=niacinamide)...")
    res = client.get('/shop/?q=niacinamide')
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    search_count = len(res.context['products'])
    assert search_count >= 1, "Search returned 0 results"
    print(f"   [+] PASS: Search for 'niacinamide' returned {search_count} product(s).")

    # 4. Test Category Filter
    print("\n4. Testing Category Filter (GET /category/face-wash/)...")
    res = client.get('/category/face-wash/')
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    cat_prods = len(res.context['products'])
    assert cat_prods >= 1, "Category filter returned 0 results"
    print(f"   [+] PASS: Face Wash category returned {cat_prods} products.")

    # 5. Test Product Detail
    print("\n5. Testing Product Detail (GET /product/<pk>/)...")
    first_product = Product.objects.first()
    assert first_product is not None, "No products found in MongoDB"
    pk_str = str(first_product.pk)
    res = client.get(f'/product/{pk_str}/')
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert res.context['product'].name == first_product.name
    print(f"   [+] PASS: Product detail view loaded '{first_product.name}' (PK: {pk_str}).")

    # 6. Test Add to Cart
    print("\n6. Testing Add to Cart (POST /cart/add/<pk>/)...")
    initial_stock = first_product.stock
    res = client.post(f'/cart/add/{pk_str}/', {'quantity': 2}, follow=True)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    session_cart = client.session.get('cart', {})
    assert pk_str in session_cart, "Product not in cart session"
    assert session_cart[pk_str] == 2, f"Expected quantity 2, got {session_cart.get(pk_str)}"
    print(f"   [+] PASS: Added 2 units of '{first_product.name}' to cart session.")

    # 7. Test Cart View
    print("\n7. Testing Cart view (GET /cart/)...")
    res = client.get('/cart/')
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert len(res.context['cart_items']) == 1
    assert res.context['cart_items'][0]['quantity'] == 2
    print(f"   [+] PASS: Cart view displayed items. Grand total: {res.context['formatted_grand_total']}")

    # 8. Test Update Cart Quantity
    print("\n8. Testing Update Cart (POST /cart/update/<pk>/)...")
    res = client.post(f'/cart/update/{pk_str}/', {'action': 'increase'}, follow=True)
    assert res.status_code == 200
    assert client.session['cart'][pk_str] == 3
    print("   [+] PASS: Quantity increased to 3.")

    # 9. Test Checkout and Order Creation
    print("\n9. Testing Checkout & Order Creation (POST /checkout/)...")
    checkout_data = {
        'full_name': 'MongoDB Test User',
        'email': 'mongo.test@example.com',
        'phone': '+91 9988776655',
        'address': 'Flat 402, Green Orchid Residency',
        'city': 'Bengaluru',
        'postal_code': '560001',
    }
    initial_order_count = Order.objects.count()
    res = client.post('/checkout/', checkout_data, follow=True)
    assert res.status_code == 200, f"Expected 200 after checkout redirect, got {res.status_code}"
    assert Order.objects.count() == initial_order_count + 1, "Order was not created in MongoDB"
    
    new_order = Order.objects.latest('created_at')
    assert new_order.full_name == 'MongoDB Test User'
    assert new_order.items.count() >= 1, "Order items were not created"
    
    # Check inventory deduction
    first_product.refresh_from_db()
    assert first_product.stock == initial_stock - 3, f"Expected stock {initial_stock - 3}, got {first_product.stock}"
    print(f"   [+] PASS: Order #{new_order.id} placed in MongoDB! Inventory deducted by 3 units.")

    # 10. Test Order Success Page
    print("\n10. Testing Order Success view...")
    res = client.get(f'/order-success/{str(new_order.id)}/')
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert res.context['order'].id == new_order.id
    print(f"   [+] PASS: Order success page rendered for Order #{new_order.id}.")

    # 11. Test Cart cleared after order
    assert client.session.get('cart') == {}, "Cart was not emptied after checkout"
    print("   [+] PASS: Cart session emptied after successful checkout.")

    print("\n" + "=" * 65)
    print("[+] ALL 11 TEST SUITES PASSED! MONGODB INTEGRATION FULLY VERIFIED.")
    print("=" * 65)

if __name__ == '__main__':
    run_tests()
