from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import ListView, DetailView, View, TemplateView
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
        print(context["variations"])
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

        return redirect("cart")


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

        return redirect("cart")


# Checkout view
class CheckoutView(TemplateView):
    template_name = "store/checkout.html"
    STRIPE_PUBLISHABLE_KEY = settings.STRIPE_PUBLISHABLE_KEY

    def get(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return self.render_to_response(
            {
                "cart_items": cart_items,
                "total_price": total_price,
                "STRIPE_PUBLISHABLE_KEY": self.STRIPE_PUBLISHABLE_KEY,
            }
        )

    def post(self, request, *args, **kwargs):
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        payment_method = request.POST.get("payment_method")

        # Create the order first (with status 'pending' initially)
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            payment_method=payment_method,
            status="pending",
        )

        # Add cart items to the order
        for item in cart_items:
            order.items.create(
                product=item.product, quantity=item.quantity, price=item.product.price
            )

        if payment_method == "stripe":
            # Create payment intent with Stripe
            intent = stripe.PaymentIntent.create(
                amount=int(total_price * 100),  # in cents
                currency="usd",
                metadata={"order_id": order.id},
            )
            client_secret = intent.client_secret
            return self.render_to_response(
                {
                    "cart_items": cart_items,
                    "total_price": total_price,
                    "client_secret": client_secret,
                    "order_id": order.id,  # Ensure the order.id is passed here
                }
            )
        else:
            # Redirect to order confirmation if paying later
            return redirect("order_confirmation", pk=order.id)


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
class OrderConfirmationView(DetailView):
    model = Order
    template_name = "store/order_confirmation.html"
    context_object_name = "order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = self.object
        return context


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
        return redirect("order_confirmation", order_id=order.id)
