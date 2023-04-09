import calendar
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Category, Brand, Product, ProductAttribute, CartOrder, CartOrderItems, ProductReview, Wishlist, UserAddressBook
from django.db.models import Max, Min, Count, Avg
from django.db.models.functions import ExtractMonth
from django.template.loader import render_to_string
from .forms import SignupForm, ReviewAdd, AddressBookForm, ProfileForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
# paypal
from django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
# Create your views here.


# home page
def home(request):
    featuredProduct = Product.objects.filter(is_featured=True).order_by('-id')
    return render(request, 'index.html', {'featuredProduct': featuredProduct})


def aboutUs(request):
    return render(request, 'about.html')


def products(request):
    data = Category.objects.all().order_by('-id')
    return render(request, 'categorylist.html', {'catlist': data})


def brands(request):
    data = Brand.objects.all()
    return render(request, 'brandlist.html', {'brandlist': data})


def product_list(request):
    total_data = Product.objects.count()
    data = Product.objects.all().order_by('-id')[:14]
    return render(request, 'products.html', {
        'productlist': data,
        'total_data': total_data,
    })


# product list accourding to category
def category_product_list(request, cat_id):
    category = Category.objects.get(id=cat_id)
    data = Product.objects.filter(category=category).order_by('-id')
    return render(request, 'category_product_list.html', {
        'productlist': data,
    })


# product list accourding to Brand
def brand_product_list(request, brand_id):
    brand = Brand.objects.get(id=brand_id)
    data = Product.objects.filter(brand=brand).order_by('-id')
    return render(request, 'category_product_list.html', {
        'productlist': data,
    })


# product details
def product_detail(request, slug, id):
    product = Product.objects.get(id=id)
    sizes = ProductAttribute.objects.filter(product=product).values(
        'size__id', 'size__title', 'price').distinct()
    reviewForm = ReviewAdd()

    # Check
    canAdd = True
    reviewCheck = ProductReview.objects.filter(
        user=request.user, product=product).count()
    if request.user.is_authenticated:
        if reviewCheck > 0:
            canAdd = False
        # End

    # Fetch reviews
    reviews = ProductReview.objects.filter(product=product)
    # End

    # Fetch avg rating for reviews
    avg_reviews = ProductReview.objects.filter(
        product=product).aggregate(avg_rating=Avg('review_rating'))
    # End

    return render(request, 'productpage.html', {'product': product, 'sizes': sizes, 'reviewForm': reviewForm, 'canAdd': canAdd, 'reviews': reviews, 'avg_reviews': avg_reviews})


# search
def search(request):
    q = request.GET['q']
    data = Product.objects.filter(title__icontains=q).order_by('-id')
    return render(request, 'search.html', {'products': data})


# filtered data
def filter_data(request):
    categories = request.GET.getlist('category[]')
    brands = request.GET.getlist('brand[]')
    sizes = request.GET.getlist('size[]')
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    allProducts = Product.objects.all().order_by('-id').distinct()
    allProducts = allProducts.filter(productattribute__price__gte=minPrice)
    allProducts = allProducts.filter(productattribute__price__lte=maxPrice)
    if len(categories) > 0:
        allProducts = allProducts.filter(
            category__id__in=categories).distinct()
    if len(brands) > 0:
        allProducts = allProducts.filter(brand__id__in=brands).distinct()
    if len(sizes) > 0:
        allProducts = allProducts.filter(
            productattribute__size__id__in=sizes).distinct()
    t = render_to_string('ajax/product-list.html', {'data': allProducts})
    return JsonResponse({'data': t})


# load more data
def load_more_data(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    data = Product.objects.all().order_by('-id')[offset:offset+limit]
    t = render_to_string('ajax/product-list.html', {'data': data})
    return JsonResponse({'data': t})


# add to cart
def add_to_cart(request):
    # del request.session['cartdata']
    cart_p = {}
    cart_p[str(request.GET['id'])] = {
        'image': request.GET['image'],
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
    }
    if 'cartdata' in request.session:
        if str(request.GET['id']) in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = int(
                cart_p[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cartdata'] = cart_data
        else:
            cart_data = request.session['cartdata']
            cart_data.update(cart_p)
            request.session['cartdata'] = cart_data
    else:
        request.session['cartdata'] = cart_p
    return JsonResponse({'data': request.session['cartdata'], 'totalitems': len(request.session['cartdata'])})


# cart list page
def cart_list(request):
    total_amt = 0
    total_amt_tax = 0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            total_amt += int(item['qty'])*float(item['price'])
        total_amt_tax = total_amt + 15
        return render(request, 'cart.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt': total_amt, 'total_amt_tax': total_amt_tax})
    else:
        return render(request, 'cart.html', {'cart_data': '', 'totalitems': 0, 'total_amt': total_amt})


# Delete Cart Item
def delete_cart_item(request):
    p_id = str(request.GET['id'])
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            del request.session['cartdata'][p_id]
            request.session['cartdata'] = cart_data
    total_amt = 0
    total_amt_tax = 0
    for p_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty'])*float(item['price'])
        total_amt_tax = total_amt + 15
    t = render_to_string('ajax/cart-list.html', {'cart_data': request.session['cartdata'], 'totalitems': len(
        request.session['cartdata']), 'total_amt': total_amt, 'total_amt_tax': total_amt_tax})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})


# Update Cart Item
def update_cart_item(request):
    p_id = str(request.GET['id'])
    p_qty = request.GET['qty']
    if 'cartdata' in request.session:
        if p_id in request.session['cartdata']:
            cart_data = request.session['cartdata']
            cart_data[str(request.GET['id'])]['qty'] = p_qty
            request.session['cartdata'] = cart_data
    total_amt = 0
    total_amt_tax = 0
    for p_id, item in request.session['cartdata'].items():
        total_amt += int(item['qty'])*float(item['price'])
        total_amt_tax = total_amt + 15
    t = render_to_string('ajax/cart-list.html', {'cart_data': request.session['cartdata'], 'totalitems': len(
        request.session['cartdata']), 'total_amt': total_amt, 'total_amt_tax': total_amt_tax})
    return JsonResponse({'data': t, 'totalitems': len(request.session['cartdata'])})


# Signup Form
def signup(request):
    form = SignupForm
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            pwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=pwd)
            login(request, user)
            return redirect('home')
    return render(request, 'registration/signup.html', {'form': form})


# checkout
@login_required
def checkout(request):
    total_amt = 0
    total_amt_tax = 0
    totalAmt = 0
    if 'cartdata' in request.session:
        for p_id, item in request.session['cartdata'].items():
            totalAmt += int(item['qty'])*float(item['price'])
        # order
        order = CartOrder.objects.create(
            user=request.user,
            total_amt=totalAmt+15
        )
        # order End
        for p_id, item in request.session['cartdata'].items():
            total_amt += int(item['qty'])*float(item['price'])
            # orderItems
            items = CartOrderItems.objects.create(
                order=order,
                invoice_no='INV-'+str(order.id),
                item=item['title'],
                image=item['image'],
                qty=item['qty'],
                price=item['price'],
                total=float(item['qty'])*float(item['price'])
            )
            # orderItems End
        total_amt_tax = total_amt + 15
        # processPayment
        host = request.get_host()
        paypal_dict = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': total_amt,
            'item_name': 'OrderNo-'+str(order.id),
            'invoice': 'INV-'+str(order.id),
            'currency_code': 'USD',
            'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
            'return_url': 'http://{}{}'.format(host, reverse('payment_done')),
            'cancel_return': 'http://{}{}'.format(host, reverse('payment_cancelled')),
        }
        form = PayPalPaymentsForm(initial=paypal_dict)
        address = UserAddressBook.objects.filter(
            user=request.user, status=True).first()
        return render(request, 'checkout.html', {'cart_data': request.session['cartdata'], 'totalitems': len(request.session['cartdata']), 'total_amt': total_amt, 'total_amt_tax': total_amt_tax, 'form': form, 'address': address})


@csrf_exempt
def payment_done(request):
    returnData = request.POST
    del request.session['cartdata']
    return render(request, 'payment-success.html', {'data': returnData})


@csrf_exempt
def payment_canceled(request):
    return render(request, 'payment-fail.html')


# Save Review
def save_review(request, pid):
    product = Product.objects.get(pk=pid)
    user = request.user
    review = ProductReview.objects.create(
        user=user,
        product=product,
        review_text=request.GET['review_text'],
        review_rating=request.GET['review_rating'],
    )
    data = {
        'user': user.username,
        'review_text': request.GET['review_text'],
        'review_rating': request.GET['review_rating']
    }

    # Fetch avg rating for reviews
    avg_reviews = ProductReview.objects.filter(
        product=product).aggregate(avg_rating=Avg('review_rating'))
    # End

    return JsonResponse({'bool': True, 'data': data, 'avg_reviews': avg_reviews})


# User Dashboard
def my_dashboard(request):
    orders = CartOrder.objects.annotate(month=ExtractMonth('order_dt')).values(
        'month').annotate(count=Count('id')).values('month', 'count')
    monthNumber = []
    totalOrders = []
    for d in orders:
        monthNumber.append(calendar.month_name[d['month']])
        totalOrders.append(d['count'])
    return render(request, 'user/dashboard.html', {'monthNumber': monthNumber, 'totalOrders': totalOrders})


# My Orders
def my_orders(request):
    orders = CartOrder.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/orders.html', {'orders': orders})


# Order Detail
def my_order_items(request, id):
    order = CartOrder.objects.get(pk=id)
    orderitems = CartOrderItems.objects.filter(order=order).order_by('-id')
    return render(request, 'user/order-items.html', {'orderitems': orderitems})


# Wishlist
def add_wishlist(request):
    pid = request.GET['product']
    product = Product.objects.get(pk=pid)
    data = {}
    checkw = Wishlist.objects.filter(
        product=product, user=request.user).count()
    if checkw > 0:
        data = {
            'bool': False
        }
    else:
        wishlist = Wishlist.objects.create(
            product=product,
            user=request.user
        )
        data = {
            'bool': True
        }
    return JsonResponse(data)


# My Wishlist
def my_wishlist(request):
    wlist = Wishlist.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/wishlist.html', {'wlist': wlist})


# My Reviews
def my_reviews(request):
    reviews = ProductReview.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/reviews.html', {'reviews': reviews})


# My AddressBook
def my_addressbook(request):
    addbook = UserAddressBook.objects.filter(user=request.user).order_by('-id')
    return render(request, 'user/addressbook.html', {'addbook': addbook})


# Save addressbook
def save_address(request):
    msg = None
    if request.method == 'POST':
        form = AddressBookForm(request.POST)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            if 'status' in request.POST:
                UserAddressBook.objects.update(status=False)
            saveForm.save()
            msg = 'Data has been saved'
    form = AddressBookForm
    return render(request, 'user/add-address.html', {'form': form, 'msg': msg})


# Activate address
def activate_address(request):
    a_id = str(request.GET['id'])
    UserAddressBook.objects.update(status=False)
    UserAddressBook.objects.filter(id=a_id).update(status=True)
    return JsonResponse({'bool': True})


# Edit Profile
def edit_profile(request):
    msg = None
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            msg = 'Data has been saved'
    form = ProfileForm(instance=request.user)
    return render(request, 'user/edit-profile.html', {'form': form, 'msg': msg})


# Update addressbook
def update_address(request, id):
    address = UserAddressBook.objects.get(pk=id)
    msg = None
    if request.method == 'POST':
        form = AddressBookForm(request.POST, instance=address)
        if form.is_valid():
            saveForm = form.save(commit=False)
            saveForm.user = request.user
            if 'status' in request.POST:
                UserAddressBook.objects.update(status=False)
            saveForm.save()
            msg = 'Data has been saved'
    form = AddressBookForm(instance=address)
    return render(request, 'user/update-address.html', {'form': form, 'msg': msg})
