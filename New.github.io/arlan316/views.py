import uuid
from django.shortcuts import render, redirect
from .models import Product, Category, Transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .midtrans import get_snap_client
from django.conf import settings  # Pastikan untuk mengimpor settings

def category(request, foo):
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)  # Perbaiki variabel dari 'product' ke 'products'
        return render(request, 'category.html', {'products': products, 'category': category})
    except Category.DoesNotExist:
        messages.error(request, "That category doesn't exist.")
        return redirect('home')

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})

def home_view(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')
        else:
            messages.error(request, "There was an error, please try again.")
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "You have logged out.")
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # Log in user 
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have registered successfully!")
            return redirect('home')
        else:
            messages.error(request, "There was a problem registering, please try again.")
            return redirect('register')
    else:
        return render(request, 'register.html', {'form': form})

def create_transaction(request):
    if request.method == "POST":
        amount = request.POST.get('amount')

        # Buat order ID unik
        order_id = str(uuid.uuid4())

        # Simpan transaksi ke database
        transaction = Transaction.objects.create(
            order_id=order_id,
            gross_amount=amount,
        )

        # Dapatkan token pembayaran dari Midtrans
        snap = get_snap_client()
        transaction_params = {
            "transaction_details": {
                "order_id": transaction.order_id,
                "gross_amount": float(amount),
            },
            "credit_card": {
                "secure": True
            },
        }
        snap_token = snap.create_transaction(transaction_params)['token']

        return render(request, 'payment_page.html', {
            'snap_token': snap_token,
            'client_key': settings.MIDTRANS_CLIENT_KEY  # Pastikan Anda memiliki client_key di settings
        })

    return render(request, 'create_transaction.html')














# import uuid
# from django.shortcuts import render, redirect
# from .models import Product, Category, Transaction
# from django.contrib.auth import authenticate, login, logout
# from django.contrib import messages
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
# from .forms import SignUpForm
# from django import forms
# from .midtrans import get_snap_client
# from django.conf import settings

# def category(request,foo):
#     foo = foo.replace('-', ' ')
#     try:
#         category = Category.objects.get(name=foo)
#         product = Product.objects.filter(category=category)
#         return render(request, 'category.html', {'products': products, 'category': category})
#     except:
#         messages.success(request, ("that Category Doesn't Exist..."))
#         return redirect('home')


# def product(request, pk):
#     product = Product.objects.get(id=pk)
#     return render(request,'product.html', {'product': product })


# def home_view(request):
#     products = Product.objects.all()
#     return render(request,'home.html', {'products': products})

# def about(request):
#     return render(request,'about.html', {})

# def login_user(request):
#     if request.method == "POST":
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             messages.success(request, ("Your Have Been Logged in!"))
#             return redirect('home')
#         else:
#             messages.success(request, ("There was an error, please try again.."))
#             return redirect('login')

#     else:
#         return render(request,'login.html', {})

# def logout_user(request):
#     logout(request)
#     messages.success(request, ("You have logged out"))
#     return redirect('home')

# def register_user(request):
#     form = SignUpForm()
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             # log in user 
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             messages.success(request, ("You have register successfully!!"))
#             return redirect('home')
#         else:
#             messages.success(request, ("there was a problem Registering, plase try again!!"))
#             return redirect('register')
#     else:
#         return render(request, 'register.html', {'form':form})

#     def create_transaction(request):
#     if request.method == "POST":
#         amount = request.POST.get('amount')

        # Buat order ID unik
        # order_id = str(uuid.uuid4())

        # Simpan transaksi ke database
        # transaction = Transaction.objects.create(
        #     order_id=order_id,
        #     gross_amount=amount,
        # )

        # Dapatkan token pembayaran dari Midtrans
        # snap = get_snap_client()
        # transaction_params = {
        #     "transaction_details": {
        #         "order_id": transaction.order_id,
        #         "gross_amount": float(amount),
        #     },
        #     "credit_card": {
        #         "secure": True
        #     },
        # }
        # snap_token = snap.create_transaction(transaction_params)['token']

        # return render(request, 'payment_page.html', {
        #     'snap_token': snap_token,
        #     'client_key': settings.MIDTRANS_CLIENT_KEY  # Pastikan Anda memiliki client_key di settings
        # })

    # return render(request, 'create_transaction.html')