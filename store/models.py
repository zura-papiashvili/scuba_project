from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    SALE = "sale"
    RENT = "rent"
    BOTH = "both"

    PRODUCT_TYPE_CHOICES = [
        (SALE, _("For Sale")),
        (RENT, _("For Rent")),
        (BOTH, _("Both Sale & Rent")),
    ]

    name = models.CharField(_("Name"), max_length=255)
    description = models.TextField(_("Description"), blank=True, null=True)
    price = models.DecimalField(
        _("Purchase Price"), max_digits=10, decimal_places=2, blank=True, null=True
    )
    rental_price_per_day = models.DecimalField(
        _("Rental Price Per Day"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    product_type = models.CharField(
        _("Product Type"), max_length=10, choices=PRODUCT_TYPE_CHOICES, default=SALE
    )
    stock = models.PositiveIntegerField(_("Stock"), default=0)
    size = models.CharField(_("Size"), max_length=50, blank=True, null=True)  # Optional
    color = models.CharField(
        _("Color"), max_length=50, blank=True, null=True
    )  # Optional
    thickness = models.DecimalField(
        _("Thickness (mm)"), max_digits=5, decimal_places=2, blank=True, null=True
    )  # Optional
    weight = models.DecimalField(
        _("Weight (kg)"), max_digits=5, decimal_places=2, blank=True, null=True
    )  # Optional
    material = models.CharField(
        _("Material"), max_length=100, blank=True, null=True
    )  # Optional
    brand = models.CharField(
        _("Brand"), max_length=100, blank=True, null=True
    )  # Optional
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def __str__(self):
        return self.name


class Variation(models.Model):
    product = models.ForeignKey(
        Product, related_name="variations", on_delete=models.CASCADE
    )
    size = models.CharField(_("Size"), max_length=50, blank=True, null=True)
    color = models.CharField(_("Color"), max_length=50, blank=True, null=True)
    thickness = models.DecimalField(
        _("Thickness (mm)"), max_digits=5, decimal_places=2, blank=True, null=True
    )
    stock = models.PositiveIntegerField(_("Stock"), default=0)
    price = models.DecimalField(
        _("Price"), max_digits=10, decimal_places=2, blank=True, null=True
    )  # Optional
    rental_price_per_day = models.DecimalField(
        _("Rental Price Per Day"),
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )  # Optional
    weight = models.DecimalField(
        _("Weight (kg)"), max_digits=5, decimal_places=2, blank=True, null=True
    )  # Optional

    def __str__(self):
        return (
            f"Variation of {self.product.name} - Size: {self.size}, Color: {self.color}"
        )


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(_("Image"), upload_to="products/images/")
    is_main = models.BooleanField(_("Is Main Image"), default=False)

    def __str__(self):
        return f"{self.product.name} - {self.id} Image"


class CartItem(models.Model):
    user = models.ForeignKey(
        User, related_name="cart_items", on_delete=models.CASCADE, null=True
    )
    product = models.ForeignKey(
        Product, related_name="cart_items", on_delete=models.CASCADE
    )
    variation = models.ForeignKey(
        Variation,
        related_name="cart_items",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    quantity = models.PositiveIntegerField(_("Quantity"), default=1)
    selected_size = models.CharField(_("Size"), max_length=50, blank=True, null=True)
    selected_color = models.CharField(_("Color"), max_length=50, blank=True, null=True)

    def __str__(self):
        return f"CartItem for {self.product.name} - Size: {self.selected_size}, Color: {self.selected_color}"


class Order(models.Model):
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    status = models.CharField(_("Status"), max_length=50, default="Pending")

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="order_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    variation = models.ForeignKey(
        Variation,
        related_name="order_items",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    quantity = models.PositiveIntegerField(_("Quantity"))
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)

    def __str__(self):
        return f"OrderItem for {self.product.name} - Quantity: {self.quantity}"


class Payment(models.Model):
    STRIPE = "stripe"
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"

    PAYMENT_METHOD_CHOICES = [
        (STRIPE, _("Stripe")),
        (CASH, _("Cash")),
        (BANK_TRANSFER, _("Bank Transfer")),
    ]

    order = models.OneToOneField(
        Order, related_name="payment", on_delete=models.CASCADE
    )
    payment_date = models.DateTimeField(_("Payment Date"), auto_now_add=True)
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)
    status = models.CharField(_("Payment Status"), max_length=50, default="Pending")
    payment_method = models.CharField(
        _("Payment Method"),
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default=STRIPE,
    )
    transaction_id = models.CharField(
        _("Transaction ID"), max_length=255, blank=True, null=True
    )  # Optional, for Stripe or other payment gateways

    def __str__(self):
        return f"Payment for Order {self.order.id} - Status: {self.status} via {self.get_payment_method_display()}"
