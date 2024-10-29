from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout 
from .models import Product, CartItem
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'index.html')

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        mobile = request.POST['mobile']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        user = User.objects.create_user(username, email, pass1 )
        user.first_name = fname
        user.save()

        messages.success(request, "YOUR ACCONT IS CREATED")
        return redirect('login')

    return render(request, "registration/signup.html")


def user_login(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None :
            auth_login(request, user)
            fname = user.first_name
            return render(request, "dashboard.html")

        else:
            messages.error(request, "Invalid Credentials")
            return redirect('login')
        
    return render(request, "registration/login.html")

def user_logout(request):
    auth_logout(request)
    return render(request, 'index.html')

@login_required
def dashboard(request):
    products = Product.objects.all()  
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = sum(item.total_price() for item in cart_items)
    return render(request, "dashboard.html", {
        'products': products,
        'cart_items': cart_items,
        'total_amount': total_amount
    })



@login_required
def add_product(request):
    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        image = request.FILES.get('image')
        Product.objects.create(name=name, price=price, image=image)
        return redirect('dashboard')
    return render(request, 'add_product.html')


@login_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        product.name = request.POST['name']
        product.price = request.POST['price']
        if request.FILES.get('image'):
            product.image = request.FILES['image']
        product.save()
        return redirect('dashboard')
    return render(request, 'edit_product.html', {'product': product})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('dashboard')



@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('dashboard')


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_amount': total_amount})

@login_required
def addandedit(request):
    products = Product.objects.all()  
    cart_items = CartItem.objects.filter(user=request.user)

    return render(request, "addandedit.html", {
        'products': products,
        'cart_items': cart_items,
    })

