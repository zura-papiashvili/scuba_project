from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from .models import Product, Variation, CartItem, Order, OrderItem, Payment
from django.conf import settings
import stripe

stripe.api_key = (
    settings.STRIPE_SECRET_KEY
)  # Ensure your Stripe secret key is in settings


# Product list view
class ProductListView(ListView):
    model = Product
    template_name = "store/product_list.html"
    context_object_name = "products"


# Product detail view
class ProductDetailView(DetailView):
    model = Product
    template_name = "store/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context["variations"] = product.variations.all()
        return context


# Add product to cart view
class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        variation_id = request.POST.get("variation_id")
        variation = None
        if variation_id:
            variation = get_object_or_404(Variation, id=variation_id)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            variation=variation,
            defaults={"quantity": 1},
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect("store:cart")


# Cart view
class CartView(LoginRequiredMixin, ListView):
    model = CartItem
    template_name = "store/cart.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = context["cart_items"]
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        context["total_price"] = total_price
        return context


# Update cart view
class UpdateCartView(LoginRequiredMixin, View):
    def post(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
        quantity = int(request.POST.get("quantity"))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()

        return redirect("store:cart")


# Checkout view
class CheckoutView(LoginRequiredMixin, View):
    def get(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return render(
            request,
            "store/checkout.html",
            {"cart_items": cart_items, "total_price": total_price},
        )


# Stripe payment view
class CreatePaymentView(LoginRequiredMixin, View):
    def post(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Create a payment intent with Stripe
        intent = stripe.PaymentIntent.create(
            amount=int(total_price * 100),  # Amount is in cents
            currency="usd",
            metadata={"user_id": request.user.id},
        )

        return JsonResponse({"client_secret": intent.client_secret})


# Order confirmation view
class OrderConfirmationView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "store/order_confirmation.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# Create order view
class CreateOrderView(LoginRequiredMixin, View):
    def post(self, request):
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Create the order
        order = Order.objects.create(user=request.user, total_price=total_price)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                variation=item.variation,
                quantity=item.quantity,
                price=item.product.price,
            )

        # Mark cart items as ordered and clear the cart
        cart_items.delete()
        return redirect("store:order_confirmation", order_id=order.id)
