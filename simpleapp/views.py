from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from .models import Category, Product, Order, OrderItem
from .forms import (
    ProductForm, UserRegistrationForm, UserLoginForm,
    CheckoutForm, ContactForm
)

def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


# --------------------------------------------------------------------------
# HOME & STATIC PAGES
# --------------------------------------------------------------------------

def home_view(request):
    """Homepage with Bootstrap 5 skincare carousel, bestsellers, and trust pillars."""
    bestsellers = Product.objects.all().order_by('-rating', '-created_at')[:4]
    categories = Category.objects.all()

    # Three attractive skincare carousel banners
    carousel_slides = [
        {
            'image': 'https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?w=1600&auto=format&fit=crop&q=80',
            'title': 'Kind to Skin. Powerful on Results.',
            'subtitle': '0% harsh chemicals, artificial perfumes, or drying alcohols. Dermatologically tested for sensitive skin.',
            'button_text': 'Shop Bestsellers',
            'button_url': '/shop/',
            'badge': '100% Soap-Free & Vegan'
        },
        {
            'image': 'https://images.unsplash.com/photo-1598440947619-2c35fc9aa908?w=1600&auto=format&fit=crop&q=80',
            'title': 'Intense Hydration Barrier Boost',
            'subtitle': 'Enriched with Pro-Vitamin B5 and botanical ceramides to restore hydration for up to 24 hours.',
            'button_text': 'Explore Moisturizers',
            'button_url': '/category/moisturizers/',
            'badge': 'Dermatologist Certified'
        },
        {
            'image': '/static/images/booster-serum-banner.jpg',
            'title': 'Gentle High-Potency Booster Serums',
            'subtitle': 'Target redness, dullness, and dehydration with concentrated Niacinamide and Hyaluronic Acid drops.',
            'button_text': 'Discover Serums',
            'button_url': '/category/serums/',
            'badge': 'Barrier Friendly'
        }
    ]

    return render(request, 'home.html', {
        'carousel_slides': carousel_slides,
        'bestsellers': bestsellers,
        'categories': categories,
    })


def shop_view(request):
    """Full product catalog with search, category filtering, and sorting."""
    products = Product.objects.all()
    categories = Category.objects.all()

    # Search by product name or description
    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredients__icontains=query)
        )

    # Category filter
    category_slug = request.GET.get('category', '').strip()
    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=active_category)

    # Skin Type filter
    skin_type = request.GET.get('skin_type', '').strip()
    if skin_type:
        products = products.filter(skin_type=skin_type)

    # Sorting
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-rating')
    else:
        products = products.order_by('-created_at')

    return render(request, 'shop.html', {
        'products': products,
        'categories': categories,
        'active_category': active_category,
        'search_query': query,
        'current_sort': sort,
        'current_skin_type': skin_type,
    })


def category_view(request, slug):
    """Filtered view by specific category."""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'shop.html', {
        'products': products,
        'categories': Category.objects.all(),
        'active_category': category,
        'is_category_page': True,
    })


def product_detail_view(request, pk):
    """Single product view with ingredients, stock, and related products."""
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)[:3]
    return render(request, 'product_detail.html', {
        'product': product,
        'related_products': related_products,
    })


def about_view(request):
    """Brand mission, 0% harsh chemical pledge, and philosophy."""
    return render(request, 'about.html')


def contact_view(request):
    """Customer care inquiries and skin routine questions."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            messages.success(
                request,
                f"Thank you, {form.cleaned_data['full_name']}! Our sensitive skincare specialists have received your message and will reply within 24 hours."
            )
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


# --------------------------------------------------------------------------
# SHOPPING CART & DEMO CHECKOUT
# --------------------------------------------------------------------------

def cart_view(request):
    """Cart view calculating item subtotals, shipping, and grand total in INR."""
    cart = request.session.get('cart', {})
    cart_items = []
    subtotal = Decimal('0.00')

    for pid_str, quantity in cart.items():
        try:
            pid = int(pid_str)
            product = Product.objects.get(id=pid)
            qty = int(quantity)
            item_total = product.price * qty
            subtotal += item_total
            cart_items.append({
                'product': product,
                'quantity': qty,
                'item_total': item_total,
                'formatted_item_total': f"₹{item_total:,.2f}",
            })
        except (Product.DoesNotExist, ValueError):
            continue

    # Free shipping on orders over ₹999; otherwise ₹99 delivery fee
    free_shipping_threshold = Decimal('999.00')
    shipping_cost = Decimal('0.00') if subtotal >= free_shipping_threshold or subtotal == 0 else Decimal('99.00')
    grand_total = subtotal + shipping_cost

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'formatted_subtotal': f"₹{subtotal:,.2f}",
        'shipping_cost': shipping_cost,
        'formatted_shipping': "FREE" if shipping_cost == 0 and subtotal > 0 else f"₹{shipping_cost:,.2f}",
        'grand_total': grand_total,
        'formatted_grand_total': f"₹{grand_total:,.2f}",
        'free_shipping_threshold': free_shipping_threshold,
        'amount_needed_for_free_shipping': max(Decimal('0.00'), free_shipping_threshold - subtotal),
    })


def add_to_cart(request, pk):
    """Adds a product to the cart session."""
    product = get_object_or_404(Product, pk=pk)
    
    if not product.in_stock:
        messages.error(request, f"Sorry, {product.name} is currently out of stock.")
        return redirect(request.META.get('HTTP_REFERER', 'shop'))

    try:
        qty = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        qty = 1

    cart = request.session.get('cart', {})
    pid_str = str(product.pk)
    current_qty = cart.get(pid_str, 0)
    new_qty = current_qty + qty

    # Stock validation
    if new_qty > product.stock:
        messages.warning(
            request,
            f"Only {product.stock} units of {product.name} are available. Added maximum stock to bag."
        )
        cart[pid_str] = product.stock
    else:
        cart[pid_str] = new_qty
        messages.success(request, f"Added {qty}x {product.name} to your bag!")

    request.session['cart'] = cart
    request.session.modified = True

    next_url = request.POST.get('next')
    if next_url:
        return redirect(next_url)
    return redirect('cart')


def update_cart(request, pk):
    """Updates quantity of an item in the cart."""
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    pid_str = str(product.pk)

    if request.method == 'POST':
        action = request.POST.get('action')
        current_qty = cart.get(pid_str, 1)

        if action == 'increase':
            if current_qty + 1 <= product.stock:
                cart[pid_str] = current_qty + 1
            else:
                messages.warning(request, f"Cannot add more. Only {product.stock} units available.")
        elif action == 'decrease':
            if current_qty - 1 > 0:
                cart[pid_str] = current_qty - 1
            else:
                cart.pop(pid_str, None)
                messages.info(request, f"Removed {product.name} from bag.")
        elif action == 'set':
            try:
                new_qty = int(request.POST.get('quantity', 1))
                if new_qty <= 0:
                    cart.pop(pid_str, None)
                elif new_qty > product.stock:
                    cart[pid_str] = product.stock
                    messages.warning(request, f"Adjusted to available stock ({product.stock} units).")
                else:
                    cart[pid_str] = new_qty
            except (ValueError, TypeError):
                pass

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart')


def remove_from_cart(request, pk):
    """Removes a product completely from the cart."""
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    pid_str = str(product.pk)

    if pid_str in cart:
        cart.pop(pid_str)
        request.session['cart'] = cart
        request.session.modified = True
        messages.info(request, f"Removed {product.name} from your bag.")

    return redirect('cart')


def checkout_view(request):
    """Demo checkout without real payments; creates Order & OrderItems, deducts stock."""
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your bag is empty. Please add items before checking out.")
        return redirect('shop')

    subtotal = Decimal('0.00')
    cart_items = []
    for pid_str, quantity in cart.items():
        try:
            p = Product.objects.get(id=int(pid_str))
            qty = int(quantity)
            subtotal += p.price * qty
            cart_items.append({'product': p, 'quantity': qty})
        except (Product.DoesNotExist, ValueError):
            continue

    shipping_cost = Decimal('0.00') if subtotal >= Decimal('999.00') else Decimal('99.00')
    grand_total = subtotal + shipping_cost

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.total_amount = grand_total
            order.status = 'Confirmed'
            order.save()

            # Create order items & deduct stock
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['product'].price,
                    quantity=item['quantity']
                )
                # Deduct inventory
                p = item['product']
                p.stock = max(0, p.stock - item['quantity'])
                p.save()

            # Clear session cart
            request.session['cart'] = {}
            request.session.modified = True

            messages.success(request, f"Order #{order.id} placed successfully! Thank you for choosing Glow & Care.")
            return redirect('order_success', order_id=order.id)
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                'email': request.user.email,
            }
        form = CheckoutForm(initial=initial_data)

    return render(request, 'checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'grand_total': grand_total,
        'formatted_grand_total': f"₹{grand_total:,.2f}",
    })


def order_success_view(request, order_id):
    """Order confirmation page."""
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_success.html', {'order': order})


# --------------------------------------------------------------------------
# PRODUCT CRUD (ADMIN / STAFF ONLY)
# --------------------------------------------------------------------------

@user_passes_test(is_admin, login_url='login')
def product_create_view(request):
    """Admin-only view to add a new product."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product.name}' created successfully!")
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()

    return render(request, 'product_form.html', {
        'form': form,
        'action_title': 'Add New Skincare Product',
        'is_new': True,
    })


@user_passes_test(is_admin, login_url='login')
def product_update_view(request, pk):
    """Admin-only view to edit an existing product."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.name}' updated successfully!")
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(request, 'product_form.html', {
        'form': form,
        'product': product,
        'action_title': f"Edit '{product.name}'",
        'is_new': False,
    })


@user_passes_test(is_admin, login_url='login')
def product_delete_view(request, pk):
    """Admin-only view to delete a product with confirmation."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f"Product '{name}' was deleted successfully.")
        return redirect('shop')

    return render(request, 'product_confirm_delete.html', {'product': product})


# --------------------------------------------------------------------------
# AUTHENTICATION (REGISTER, LOGIN, LOGOUT)
# --------------------------------------------------------------------------

def register_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            messages.success(request, f"Welcome to Glow & Care, {user.first_name or user.username}!")
            return redirect('home')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """User logout view."""
    logout(request)
    messages.info(request, "You have been safely signed out. See you soon!")
    return redirect('home')
