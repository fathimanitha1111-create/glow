from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('', views.home_view, name='home'),
    path('shop/', views.shop_view, name='shop'),
    path('category/<slug:slug>/', views.category_view, name='category'),
    path('product/<str:pk>/', views.product_detail_view, name='product_detail'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),

    # Shopping Cart
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<str:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<str:pk>/', views.update_cart, name='update_cart'),
    path('cart/remove/<str:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-success/<str:order_id>/', views.order_success_view, name='order_success'),
    path('my-orders/', views.order_history_view, name='order_history'),

    # Product CRUD (Staff/Admin)
    path('product/add/', views.product_create_view, name='product_create'),
    path('product/<str:pk>/edit/', views.product_update_view, name='product_edit'),
    path('product/<str:pk>/delete/', views.product_delete_view, name='product_delete'),

    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
