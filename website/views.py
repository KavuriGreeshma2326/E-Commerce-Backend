# website/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Product, CartItem
from .forms import SignupForm
from django.contrib import messages

def home(request):
    products = Product.objects.all()
    return render(request, "website/home.html", {"products": products})

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignupForm()
    return render(request, "website/users/signup.html", {"form": form})

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, "website/products/product_list.html", {"products": products})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        qty = int(request.POST.get("quantity", 1))
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        cart_item.quantity += qty
        cart_item.save()
        return redirect("cart")
    return render(request, "website/products/product_detail.html", {"product": product})

@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in items)
    return render(request, "website/cart.html", {"items": items, "total": total})

@login_required
def remove_from_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    item.delete()
    return redirect("cart")

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect("cart")

    cart_items.delete()
    return render(request, "website/checkout.html")

