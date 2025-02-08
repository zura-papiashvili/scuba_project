from django.contrib import admin
from .models import (
    Product,
    Variation,
    ProductImage,
    CartItem,
    Order,
    OrderItem,
    Payment,
)
from modeltranslation.admin import TranslationAdmin


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = (
        "name",
        "price",
        "product_type",
        "stock",
        "created_at",
        "updated_at",
    )
    search_fields = ("name", "description", "brand")
    list_filter = ("product_type", "stock", "created_at", "updated_at")
    inlines = [ProductImageInline, VariationInline]


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "size",
        "color",
        "stock",
        "price",
        "rental_price_per_day",
    )
    search_fields = ("product__name", "size", "color")
    list_filter = ("product", "size", "color")


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("product", "is_main", "image")
    search_fields = ("product__name",)
    list_filter = ("product", "is_main")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "variation",
        "quantity",
        "selected_size",
        "selected_color",
    )
    search_fields = ("product__name", "variation__size", "variation__color")
    list_filter = ("product", "variation")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "status", "updated_at")
    search_fields = ("user__username", "status")
    list_filter = ("status", "created_at", "updated_at")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "variation", "quantity", "price")
    search_fields = ("order__id", "product__name")
    list_filter = ("order", "product")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "payment_method", "amount", "payment_date", "status")
    search_fields = ("order__id", "payment_method", "status")
    list_filter = ("payment_method", "status", "payment_date")
