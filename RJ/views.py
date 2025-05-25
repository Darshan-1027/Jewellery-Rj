from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password

from .models import *
from .forms import OrderForm  # Make sure you have this form in forms.py


def HomePage(request):
    Categorys = CategorysModel.objects.all().order_by('-id')
    context = {
        "category": Categorys
    }
    return render(request, "Homepage.html", context)


def ProductsPage(request, id):
    categories = CategorysModel.objects.all().order_by('-id')
    selected_category = get_object_or_404(CategorysModel, id=id)
    products = ProductModel.objects.filter(Category=selected_category)

    context = {
        "category": categories,
        "sub_product": products,
        "selected_category": selected_category
    }
    return render(request, "Category.html", context)


def LoginPage(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = RegisterDataModel.objects.filter(email=email).first()

        if user and check_password(password, user.password):
            request.session["user_id"] = user.id
            request.session["fname"] = user.first_name
            request.session["lname"] = user.last_name
            request.session["email"] = user.email
            request.session["phone"] = user.phone
            request.session["address"] = user.address
            return redirect("/")
        else:
            messages.error(request, "Invalid Email Id or Password")

    return render(request, "Login.html")


def Logout(request):
    request.session.flush()  # Clear all session data
    return redirect("/")


def OTPage(request):
    return render(request, "OTP.html")


def ProfilePage(request):
    return render(request, "Profile.html")


def RegisterPage(request):
    if request.method == "POST":
        first = request.POST.get("first_name")
        last = request.POST.get("last_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        address = request.POST.get("address")

        if RegisterDataModel.objects.filter(email=email).exists():
            messages.error(request, "This email already exists")
        else:
            hashed_password = make_password(password)  # Hash password
            Storedata = RegisterDataModel(
                first_name=first,
                last_name=last,
                email=email,
                phone=phone,
                password=hashed_password,
                address=address
            )
            Storedata.save()
            messages.success(request, "Registered successfully. Now you can log in.")
            return redirect("/login")

    return render(request, "Register.html")


def SingleProductPage(request, id):
    Categorys = CategorysModel.objects.all().order_by('-id')
    Product_Details = get_object_or_404(ProductModel, id=id)
    selected_category = Product_Details.Category
    products = ProductModel.objects.filter(Category=selected_category).exclude(id=id)

    context = {
        "category": Categorys,
        "sub_cat": products,
        "data": Product_Details
    }
    return render(request, "SingleProduct.html", context)


def Searchdata(request):
    if request.method == "POST":
        search = request.POST.get("search", "").strip()

        if not search:
            return redirect('/')

        product = ProductModel.objects.filter(
            Q(Name__iexact=search) | Q(Category__Name__iexact=search)
        ).first()

        if product:
            return redirect(f"/category/{product.Category.id}/")

    return redirect('/')


def add_to_cart(request, product_id):
    if not request.session.get('user_id'):
        messages.error(request, "You need to log in to add items to your cart.")
        return redirect('/login')

    user_id = request.session['user_id']
    user = get_object_or_404(RegisterDataModel, id=user_id)
    product = get_object_or_404(ProductModel, id=product_id)

    cart, created = Cart.objects.get_or_create(user=user)

    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"Added {product.Name} to cart.")
    return redirect('/cart')


def view_cart(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request, 'cart.html', {'cart_items': []})

    user = get_object_or_404(RegisterDataModel, id=user_id)

    try:
        cart = Cart.objects.get(user=user)
    except Cart.DoesNotExist:
        return render(request, 'cart.html', {'cart_items': []})

    cart_items = CartItem.objects.filter(cart=cart)

    total_price = sum(item.product.Price * item.quantity for item in cart_items)

    for item in cart_items:
        item.subtotal = item.product.Price * item.quantity

    form = OrderForm()  # Add your order form here to show in cart page if needed

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form
    })


from django.views.decorators.http import require_POST

@require_POST
def remove_from_cart(request, product_id):
    if not request.session.get('user_id'):
        messages.error(request, "You need to log in to manage your cart.")
        return redirect('/login')

    user_id = request.session['user_id']
    user = get_object_or_404(RegisterDataModel, id=user_id)
    
    try:
        cart = Cart.objects.get(user=user)
        cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        messages.error(request, "Item not found in your cart.")
    
    return redirect('view_cart')


from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Cart, CartItem, Order, OrderItem, RegisterDataModel
from .forms import OrderForm  # Make sure this form exists and has name, phone, state, city, pincode, address fields

@require_POST
def place_order(request):
    form = OrderForm(request.POST)
    if form.is_valid():
        user_id = request.session.get('user_id')
        if not user_id:
            messages.error(request, "Please login to place an order.")
            return redirect('/login')

        user = get_object_or_404(RegisterDataModel, id=user_id)

        # Create the order with correct field names
        order = Order.objects.create(
            customer_name=form.cleaned_data['name'],
            phone_number=form.cleaned_data['phone'],
            state=form.cleaned_data['state'],
            city=form.cleaned_data['city'],
            pincode=form.cleaned_data['pincode'],
            address=form.cleaned_data['address'],
        )

        # Get the user's cart and cart items
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            messages.error(request, "Your cart is empty.")
            return redirect('/cart')

        cart_items = CartItem.objects.filter(cart=cart)

        # Create OrderItems for each cart item
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.Price,
            )

        # Clear the cart after placing order
        cart_items.delete()

        messages.success(request, "Order placed successfully!")
        return redirect('order_success')  # Make sure this URL name exists in your urls.py

    else:
        messages.error(request, "Please correct the errors below.")

    return render(request, 'place_order.html', {'form': form})



def order_success(request):
    Categorys = CategorysModel.objects.all().order_by('-id')
    context = {
        "category": Categorys
    }
    return render(request, 'order_success.html',context)
