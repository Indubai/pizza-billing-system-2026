from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Sum
from django.utils import timezone

from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Order

import random
import string
import uuid


# =====================================
# PIZZA PRICES
# =====================================

pizza_prices = {
    "Small": {"Veg": 149, "Non-Veg": 199},
    "Medium": {"Veg": 249, "Non-Veg": 299},
    "Large": {"Veg": 349, "Non-Veg": 399}
}


# =====================================
# PIZZA FLAVOURS
# =====================================

pizza_flavours = {
    "Veg": ["Margherita", "Farmhouse", "Veggie Delight"],
    "Non-Veg": ["Chicken Tikka", "BBQ", "Pepperoni"]
}


# =====================================
# PIZZA BASE PRICES
# =====================================

base_prices = {
    "Classic": 0,
    "Thin Crust": 30,
    "Cheese Burst": 60
}


# =====================================
# TOPPING PRICES
# =====================================

topping_prices = {
    "Extra Cheese": 40,
    "Extra Veggies": 30
}


# =====================================
# ADDITIONAL FOOD MENU
# =====================================

menu = {
    "Drinks": {
        "Coke": 50,
        "Lemonade": 40,
        "Cold Coffee": 80
    },
    "Snacks": {
        "Nuggets": 110,
        "Fries": 90,
        "Garlic Bread": 100
    },
    "Desserts": {
        "Ice Cream": 70,
        "Cake": 120,
        "Brownie": 90
    }
}


# =====================================
# FOOD IMAGES
# =====================================

menu_images = {
    "Coke": "orders/images/coke.jpg",
    "Lemonade": "orders/images/lemonade.jpg",
    "Cold Coffee": "orders/images/coldcoffee.jpg",
    "Nuggets": "orders/images/nuggets.jpg",
    "Fries": "orders/images/fries.jpg",
    "Garlic Bread": "orders/images/garlicbread.jpg",
    "Ice Cream": "orders/images/icecream.jpg",
    "Cake": "orders/images/cake.jpg",
    "Brownie": "orders/images/brownie.jpg"
}


# =====================================
# GENERATE UNIQUE ORDER ID
# =====================================

def generate_order_id():

    letters = string.ascii_uppercase
    numbers = string.digits

    return ''.join(
        random.choices(letters + numbers, k=8)
    )


# =====================================
# HOME PAGE
# =====================================

def home(request):

    request.session["order_token"] = str(uuid.uuid4())

    context = {
        "pizza_prices": pizza_prices,
        "pizza_flavours": pizza_flavours,
        "veg_flavours": pizza_flavours["Veg"],
        "non_veg_flavours": pizza_flavours["Non-Veg"],
        "base_prices": base_prices,
        "topping_prices": topping_prices,
        "menu": menu,
        "menu_images": menu_images
    }

    return render(request, "orders/index.html", context)


# =====================================
# PLACE ORDER
# =====================================

def place_order(request):

    if request.method != "POST":
        return HttpResponse("Invalid request.")

    # Get the one-time submission token
    submission_token = request.POST.get("submission_token", "").strip()

    if not submission_token:
        return HttpResponse(
            "Order token missing. Please return to the home page and try again."
        )

    # Check whether this order was already submitted
    existing_order = Order.objects.filter(
        submission_token=submission_token
    ).first()

    if existing_order:
        return render(request, "orders/bill.html", {
            "customer_name": existing_order.customer_name,
            "order_id": existing_order.order_id,
            "bill_items": existing_order.bill_items,
            "subtotal": existing_order.subtotal,
            "discount": existing_order.discount,
            "final_total": existing_order.final_total
        })

    # Verify the token belongs to the current home-page session
    if request.session.get("order_token") != submission_token:
        return HttpResponse(
            "This order form has expired. Please return to the home page."
        )

    customer_name = request.POST.get("customer_name", "").strip()

    if not customer_name:
        return HttpResponse("Please enter your name.")

    bill_items = []

    # =====================================
    # MULTIPLE PIZZA SELECTION
    # =====================================

    sizes = request.POST.getlist("pizza_size")
    types = request.POST.getlist("pizza_type")
    flavours = request.POST.getlist("pizza_flavour")
    bases = request.POST.getlist("pizza_base")
    quantities = request.POST.getlist("pizza_quantity")

    # BACKWARD COMPATIBILITY

    if not sizes:
        sizes = request.POST.getlist("size")
        types = request.POST.getlist("pizza_type")
        flavours = request.POST.getlist("flavour")
        bases = request.POST.getlist("base")
        quantities = request.POST.getlist("quantity")

    if not (
        len(sizes) == len(types)
        == len(flavours) == len(bases)
        == len(quantities)
    ):
        return HttpResponse("Invalid pizza order details.")

    if not sizes:
        return HttpResponse("Please select at least one pizza.")

    if len(sizes) > 50:
        return HttpResponse("Too many pizzas in one order.")

    for index in range(len(sizes)):

        size = sizes[index]
        pizza_type = types[index]
        flavour = flavours[index]
        base = bases[index]

        if (
            size not in pizza_prices
            or pizza_type not in pizza_prices[size]
            or flavour not in pizza_flavours[pizza_type]
            or base not in base_prices
        ):
            return HttpResponse("Invalid pizza selection.")

        try:
            quantity = int(quantities[index])

            if not 1 <= quantity <= 100:
                raise ValueError

        except (ValueError, TypeError, IndexError):
            return HttpResponse("Invalid pizza quantity.")

        pizza_cost = pizza_prices[size][pizza_type]
        pizza_cost += base_prices[base]

        cheese = (
            "Yes"
            if request.POST.get(f"pizza_cheese_{index}") == "yes"
            else "No"
        )

        veggies = (
            "Yes"
            if request.POST.get(f"pizza_veggies_{index}") == "yes"
            else "No"
        )

        if cheese == "Yes":
            pizza_cost += topping_prices["Extra Cheese"]

        if veggies == "Yes":
            pizza_cost += topping_prices["Extra Veggies"]

        total_pizza_cost = pizza_cost * quantity

        bill_items.append({
            "name": f"{size} {pizza_type} {flavour}",
            "details": (
                f"Base: {base}, "
                f"Cheese: {cheese}, "
                f"Extra Veggies: {veggies}"
            ),
            "quantity": quantity,
            "price": pizza_cost,
            "total": total_pizza_cost
        })

    # =====================================
    # DRINKS, SNACKS AND DESSERTS
    # =====================================

    selected_items = request.POST.getlist("extra_items")
    selected_quantities = request.POST.getlist("extra_quantities")

    if len(selected_items) != len(selected_quantities):
        return HttpResponse("Invalid additional item details.")

    for item_name, item_quantity in zip(
        selected_items,
        selected_quantities
    ):

        item_price = None
        category = None

        for menu_category, items in menu.items():

            if item_name in items:
                item_price = items[item_name]
                category = menu_category
                break

        if item_price is None:
            return HttpResponse("Invalid food item.")

        try:
            quantity = int(item_quantity)

            if not 0 <= quantity <= 100:
                raise ValueError

        except (ValueError, TypeError):
            return HttpResponse("Invalid additional item quantity.")

        if quantity == 0:
            continue

        total_item_price = item_price * quantity

        bill_items.append({
            "name": item_name,
            "details": category,
            "quantity": quantity,
            "price": item_price,
            "total": total_item_price
        })

    # =====================================
    # CALCULATE SUBTOTAL
    # =====================================

    calculate_total = lambda item: item["total"]

    subtotal = sum(map(calculate_total, bill_items))

    # =====================================
    # DISCOUNT
    # =====================================

    if subtotal >= 1000:
        discount = round(subtotal * 0.10, 2)
    else:
        discount = 0

    # =====================================
    # FINAL TOTAL
    # =====================================

    final_total = round(subtotal - discount, 2)

    # =====================================
    # GENERATE ORDER ID
    # =====================================

    order_id = generate_order_id()

    # =====================================
    # PAYMENT METHOD
    # =====================================

    payment_method = request.POST.get(
        "payment_method",
        "Cash on Delivery"
    )

    valid_methods = [
        choice[0] for choice in Order.PAYMENT_CHOICES
    ]

    if payment_method not in valid_methods:
        payment_method = "Cash on Delivery"

    # =====================================
    # LINK ORDER TO CUSTOMER ACCOUNT
    # =====================================

    customer_user = (
        request.user
        if request.user.is_authenticated
        else None
    )

    # =====================================
    # SAVE ORDER WITH DUPLICATE PROTECTION
    # =====================================

    order, created = Order.objects.get_or_create(
        submission_token=submission_token,
        defaults={
            "user": customer_user,
            "customer_name": customer_name,
            "order_id": order_id,
            "bill_items": bill_items,
            "subtotal": subtotal,
            "discount": discount,
            "final_total": final_total,
            "payment_method": payment_method
        }
    )

    # Invalidate the token after a successful new order
    if created:
        request.session["order_token"] = str(uuid.uuid4())

    # =====================================
    # BILL PAGE
    # =====================================

    context = {
        "customer_name": order.customer_name,
        "order_id": order.order_id,
        "bill_items": order.bill_items,
        "subtotal": order.subtotal,
        "discount": order.discount,
        "final_total": order.final_total
    }

    return render(request, "orders/bill.html", context)


# =====================================
# ORDER HISTORY
# =====================================

def order_history(request):

    search_query = request.GET.get('search', '')
    selected_date = request.GET.get('date', '')

    orders = Order.objects.all().order_by('-created_at')

    if search_query:
        orders = orders.filter(
            customer_name__icontains=search_query
        ) | orders.filter(
            order_id__icontains=search_query
        )

    if selected_date:
        orders = orders.filter(
            created_at__date=selected_date
        )

    context = {
        "orders": orders,
        "search_query": search_query,
        "selected_date": selected_date
    }

    return render(
        request,
        'orders/order_history.html',
        context
    )


# =====================================
# ORDER DETAILS
# =====================================

def order_details(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    context = {
        "order": order,
        "bill_items": order.bill_items
    }

    return render(
        request,
        "orders/order_details.html",
        context
    )


# =====================================
# DELETE ORDER
# =====================================

def delete_order(request, order_id):

    if request.method == "POST":

        order = get_object_or_404(Order, id=order_id)
        order.delete()

    return redirect("order_history")


# =====================================
# ADMIN DASHBOARD
# =====================================

@login_required
def dashboard(request):
    if not request.user.is_staff:
        return HttpResponse("Access denied. Admin only.", status=403)

    total_orders = Order.objects.count()

    total_sales = Order.objects.aggregate(
        total=Sum('final_total')
    )['total'] or 0

    total_discounts = Order.objects.aggregate(
        total=Sum('discount')
    )['total'] or 0

    today = timezone.localdate()

    today_orders = Order.objects.filter(
        created_at__date=today
    )

    today_order_count = today_orders.count()

    today_revenue = today_orders.aggregate(
        total=Sum('final_total')
    )['total'] or 0

    recent_orders = Order.objects.all().order_by(
        '-created_at'
    )[:5]

    context = {
        'total_orders': total_orders,
        'total_sales': total_sales,
        'total_discounts': total_discounts,
        'today_order_count': today_order_count,
        'today_revenue': today_revenue,
        'recent_orders': recent_orders
    }

    return render(
        request,
        'orders/dashboard.html',
        context
    )


# =====================================
# CUSTOMER REGISTRATION
# =====================================

def register(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not username or not email or not password:
            messages.error(request, "Please fill all fields.")

        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")

        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")

        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")

        else:

            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            messages.success(
                request,
                "Registration successful! Please login."
            )

            return redirect("login")

    return render(
        request,
        "orders/register.html"
    )


# =====================================
# CUSTOMER LOGIN
# =====================================

def customer_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_active:

            login(request, user)

            return redirect("customer_dashboard")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "orders/login.html"
    )


# =====================================
# CUSTOMER LOGOUT
# =====================================

@login_required
def customer_logout(request):

    if request.method == "POST":

        logout(request)

        return redirect("home")

    return HttpResponse("Invalid request.")


# =====================================
# CUSTOMER DASHBOARD
# =====================================

@login_required
def customer_dashboard(request):

    customer_orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    context = {
        "customer_orders": customer_orders,
        "customer": request.user
    }

    return render(
        request,
        "orders/customer_dashboard.html",
        context
    )