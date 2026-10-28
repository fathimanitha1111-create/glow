from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'price', 'quantity', 'subtotal')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image_thumbnail', 'name', 'category', 'price_display', 'stock_badge', 'skin_type', 'created_at')
    list_filter = ('category', 'skin_type', 'badge', 'created_at')
    search_fields = ('name', 'description', 'ingredients')
    list_editable = ('category',)
    readonly_fields = ('created_at', 'updated_at', 'image_preview')

    def price_display(self, obj):
        return obj.formatted_price()
    price_display.short_description = 'Price (INR)'

    def stock_badge(self, obj):
        if obj.stock <= 5:
            color = 'red'
        elif obj.stock <= 15:
            color = 'orange'
        else:
            color = 'green'
        return format_html(
            '<span style="font-weight: bold; color: {};">{} units</span>',
            color, obj.stock
        )
    stock_badge.short_description = 'Stock'

    def image_thumbnail(self, obj):
        url = obj.get_image_url()
        return format_html(
            '<img src="{}" style="width: 45px; height: 45px; object-fit: cover; border-radius: 6px;" />',
            url
        )
    image_thumbnail.short_description = 'Image'

    def image_preview(self, obj):
        url = obj.get_image_url()
        return format_html(
            '<img src="{}" style="max-width: 250px; height: auto; border-radius: 8px;" />',
            url
        )
    image_preview.short_description = 'Preview'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'email', 'phone', 'formatted_total', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'full_name', 'email', 'phone', 'address')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    readonly_fields = ('order_number', 'created_at')

