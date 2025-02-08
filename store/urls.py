from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    AddToCartView,
    CartView,
    UpdateCartView,
    CheckoutView,
    CreatePaymentView,
    OrderConfirmationView,
    CreateOrderView,
)

app_name = "store"

urlpatterns = [
    # Product views
    path("products/", ProductListView.as_view(), name="product_list"),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    # Cart views
    path("cart/", CartView.as_view(), name="cart"),
    path(
        "cart/update/<int:cart_item_id>/", UpdateCartView.as_view(), name="update_cart"
    ),
    path("add_to_cart/<int:product_id>/", AddToCartView.as_view(), name="add_to_cart"),
    # Checkout and order views
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("create_payment/", CreatePaymentView.as_view(), name="create_payment"),
    path(
        "order/confirmation/<int:pk>/",
        OrderConfirmationView.as_view(),
        name="order_confirmation",
    ),
    path("create_order/", CreateOrderView.as_view(), name="create_order"),
]
