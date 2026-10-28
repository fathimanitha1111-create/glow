"""
Seed script to populate initial categories and skincare products
into the simple_db MySQL database.
"""

import os
import sys
from decimal import Decimal

# Ensure UTF-8 output on Windows consoles
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple.settings')
django.setup()

from django.db import connection
from simpleapp.models import Category, Product

def seed():
    print(f"[*] Seeding categories and products into {connection.vendor} database...")

    # 1. Categories
    categories_data = [
        {
            'name': 'Face Wash',
            'slug': 'face-wash',
            'description': '100% soap-free cleansers that remove impurities without stripping natural skin moisture.',
            'image_url': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=700&auto=format&fit=crop&q=80',
        },
        {
            'name': 'Moisturizers',
            'slug': 'moisturizers',
            'description': 'Lightweight to rich nourishing creams enriched with Pro-Vitamin B5 for up to 24 hours of comfort.',
            'image_url': 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=700&auto=format&fit=crop&q=80',
        },
        {
            'name': 'Serums',
            'slug': 'serums',
            'description': 'Targeted booster serums with high-potency, low-irritation actives to calm redness and restore radiance.',
            'image_url': 'https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=700&auto=format&fit=crop&q=80',
        },
    ]

    cat_map = {}
    for c_data in categories_data:
        cat, created = Category.objects.get_or_create(
            slug=c_data['slug'],
            defaults={
                'name': c_data['name'],
                'description': c_data['description'],
                'image_url': c_data['image_url'],
            }
        )
        cat_map[c_data['slug']] = cat
        print(f"  [Category] {cat.name} ({'Created' if created else 'Exists'})")

    # 2. Products
    products_data = [
        # Face Wash Collection
        {
            'name': 'Refreshing Facial Gel Wash',
            'category': cat_map['face-wash'],
            'price': Decimal('399.00'),
            'original_price': Decimal('499.00'),
            'stock': 35,
            'badge': 'Bestseller',
            'skin_type': 'sensitive',
            'ingredients': 'Triple Purified Water & Pro-Vitamin B5',
            'description': '100% soap-free facial wash that lifts away daily impurities, excess oil, and pollutants without stripping your delicate moisture barrier.',
            'image_url': '/static/images/refreshing-facial-gel-wash.jpg',
            'rating': Decimal('4.9'),
            'review_count': 2410,
        },
        {
            'name': 'Kind Micellar Cleansing Water',
            'category': cat_map['face-wash'],
            'price': Decimal('449.00'),
            'original_price': Decimal('549.00'),
            'stock': 28,
            'badge': 'Must-Have',
            'skin_type': 'all',
            'ingredients': 'Hexylene Glycol & Chamomile Extract',
            'description': 'Gentle micellar bubbles trap and dissolve waterproof makeup, dirt, and sebum without needing harsh rubbing or water rinsing.',
            'image_url': '/static/images/gentle-face-wash.jpg',
            'rating': Decimal('4.9'),
            'review_count': 3120,
        },
        {
            'name': 'Purifying Foaming Face Wash',
            'category': cat_map['face-wash'],
            'price': Decimal('429.00'),
            'original_price': Decimal('529.00'),
            'stock': 20,
            'badge': 'Soap-Free',
            'skin_type': 'oily',
            'ingredients': 'Thyme, Zinc PCA & Witch Hazel',
            'description': 'Gentle clarifying foam specially crafted for oily and acne-prone sensitive skin. Clears congested pores without tightness or stinging.',
            'image_url': '/static/images/purifying-foaming-face-wash.jpg',
            'rating': Decimal('4.7'),
            'review_count': 980,
        },
        {
            'name': 'Soothing Cream Cleanser',
            'category': cat_map['face-wash'],
            'price': Decimal('479.00'),
            'original_price': Decimal('599.00'),
            'stock': 15,
            'badge': 'Extra Gentle',
            'skin_type': 'dry',
            'ingredients': 'Bisabolol, Allantoin & Sweet Almond Oil',
            'description': 'Ultra-nourishing milky cleanser that melts makeup and leaves reactive, dry skin conditioned, soft, and calm.',
            'image_url': '/static/images/soothing-cream-cleanser.jpg',
            'rating': Decimal('4.8'),
            'review_count': 740,
        },

        # Moisturizers Collection
        {
            'name': 'Replenishing Rich Moisturizer',
            'category': cat_map['moisturizers'],
            'price': Decimal('599.00'),
            'original_price': Decimal('749.00'),
            'stock': 30,
            'badge': 'Barrier Boost',
            'skin_type': 'dry',
            'ingredients': 'Pro-Vitamin B5, Vitamin E & Bisabolol',
            'description': 'Deeply comforting cream that seals in hydration for up to 24 hours. Clinically proven to calm windburn, dryness, and barrier sensitivity.',
            'image_url': '/static/images/replenishing-rich-moisturizer.jpg',
            'rating': Decimal('4.8'),
            'review_count': 1890,
        },
        {
            'name': 'Hydrating Light Moisturizer',
            'category': cat_map['moisturizers'],
            'price': Decimal('499.00'),
            'original_price': Decimal('629.00'),
            'stock': 40,
            'badge': 'Daily Hero',
            'skin_type': 'sensitive',
            'ingredients': 'Borage Seed Oil, Glycerin & Pro-Vitamin B5',
            'description': 'Fast-absorbing, silk-weight lotion that leaves zero greasy residue. Ideal for everyday use under sunscreen and makeup.',
            'image_url': '/static/images/hydrating-light-moisturizer.jpg',
            'rating': Decimal('4.9'),
            'review_count': 2250,
        },
        {
            'name': 'Water Boost Hydrating Gel',
            'category': cat_map['moisturizers'],
            'price': Decimal('549.00'),
            'original_price': Decimal('699.00'),
            'stock': 25,
            'badge': 'Oil-Free',
            'skin_type': 'combination',
            'ingredients': 'Plant-Based Minerals & Pentavitin',
            'description': 'Weightless water-burst texture instantly quenches dehydrated, thirsty skin. Locks moisture into skin cells for 48 hours.',
            'image_url': '/static/images/water-booster-hydrating-gel.jpg',
            'rating': Decimal('4.7'),
            'review_count': 1120,
        },
        {
            'name': 'Restoring Night Cream',
            'category': cat_map['moisturizers'],
            'price': Decimal('649.00'),
            'original_price': Decimal('799.00'),
            'stock': 18,
            'badge': 'Overnight Repair',
            'skin_type': 'dry',
            'ingredients': 'Triple Ceramides, Shea Butter & Calendula',
            'description': 'Rich restorative night treatment that works with the skin\'s circadian rhythm to repair cellular barrier damage while you sleep.',
            'image_url': '/static/images/restoring-night-cream.jpg',
            'rating': Decimal('4.9'),
            'review_count': 860,
        },

        # Serums Collection
        {
            'name': '10% Niacinamide Clarifying Serum',
            'category': cat_map['serums'],
            'price': Decimal('699.00'),
            'original_price': Decimal('899.00'),
            'stock': 35,
            'badge': 'Best For Pores',
            'skin_type': 'oily',
            'ingredients': '10% Pure Niacinamide & 1% Zinc PCA',
            'description': 'Concentrated non-irritating booster serum that balances sebum production, refines enlarged pores, and evens out post-breakout texture.',
            'image_url': '/static/images/10-niacinamide-serum.jpg',
            'rating': Decimal('4.9'),
            'review_count': 1540,
        },
        {
            'name': 'Hyaluronic Acid 3% Serum',
            'category': cat_map['serums'],
            'price': Decimal('649.00'),
            'original_price': Decimal('799.00'),
            'stock': 30,
            'badge': 'Plumping',
            'skin_type': 'dry',
            'ingredients': 'Multi-Molecular Weight Hyaluronic Acid & B5',
            'description': 'Three molecular weights of bio-compatible hyaluronic acid penetrate multi-layer epidermis to deliver plump, dewy bounce.',
            'image_url': '/static/images/hyaluronic-acid-serum.jpg',
            'rating': Decimal('4.8'),
            'review_count': 940,
        },
        {
            'name': 'Calming Cica & B5 Barrier Drops',
            'category': cat_map['serums'],
            'price': Decimal('749.00'),
            'original_price': Decimal('949.00'),
            'stock': 22,
            'badge': 'Redness Relief',
            'skin_type': 'sensitive',
            'ingredients': 'Centella Asiatica (Cica), Madecassoside & Panthenol',
            'description': 'High-potency soothing elixir that cools irritated, flushed skin in under 15 minutes. Dermatologist tested for eczema-prone skin.',
            'image_url': '/static/images/calming-cica-b5-drops.jpg',
            'rating': Decimal('4.9'),
            'review_count': 1380,
        },
        {
            'name': 'Gentle Vitamin C Glow Serum',
            'category': cat_map['serums'],
            'price': Decimal('799.00'),
            'original_price': Decimal('999.00'),
            'stock': 20,
            'badge': 'Non-Stinging',
            'skin_type': 'all',
            'ingredients': '5% Ethyl Ascorbic Acid, Ferulic Acid & Aloe',
            'description': 'A gentle, non-acidic Vitamin C derivative that brightens dullness and defends against UV free radicals without burning sensitive skin.',
            'image_url': '/static/images/vitamin-c-glow-serum.jpg',
            'rating': Decimal('4.7'),
            'review_count': 690,
        },
    ]

    for p_data in products_data:
        p, created = Product.objects.get_or_create(
            name=p_data['name'],
            category=p_data['category'],
            defaults=p_data
        )
        print(f"  [Product] {p.name} - ₹{p.price} ({'Created' if created else 'Exists'})")

    print("\n[+] Database seeding completed successfully!")

if __name__ == '__main__':
    seed()
