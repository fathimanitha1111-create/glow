from decimal import Decimal
from .models import Category, Product

def cart_context(request):
    """
    Context processor to make cart details, active category list,
    and cart count globally accessible across all templates.
    """
    cart = request.session.get('cart', {})
    cart_total_items = 0
    cart_subtotal = Decimal('0.00')

    # Cart structure in session: {str(product_id): quantity}
    if cart:
        product_ids = [str(pid) for pid in cart.keys() if pid]
        products = Product.objects.filter(pk__in=product_ids)
        product_map = {str(p.pk): p for p in products}

        for pid_str, quantity in cart.items():
            try:
                pid = str(pid_str)
                if pid in product_map:
                    qty = int(quantity)
                    cart_total_items += qty
                    cart_subtotal += product_map[pid].price * qty
            except (ValueError, TypeError, Exception):
                continue

    categories = Category.objects.all()

    return {
        'cart_count': cart_total_items,
        'cart_subtotal_global': cart_subtotal,
        'nav_categories': categories,
    }
