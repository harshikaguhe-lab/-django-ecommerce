from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart


def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


def cart(request):
    cart_items = Cart.objects.all()

    total = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total
    })


def remove_from_cart(request, cart_id):
    item = get_object_or_404(Cart, id=cart_id)
    item.delete()
    return redirect('cart')


# ==========================
# CHECKOUT
# ==========================

def checkout(request):
    cart_items = Cart.objects.all()

    total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":
        Cart.objects.all().delete()
        return redirect('order_success')

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total
    })


# ==========================
# ORDER SUCCESS
# ==========================

def order_success(request):
    return render(request, 'store/order_success.html')