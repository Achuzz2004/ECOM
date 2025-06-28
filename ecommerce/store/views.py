from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderedItem,Review
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib import messages
from .forms import ReviewForm


def home(request):
    query = request.GET.get('q', '').strip()
    if query:
        # Filter products by name or category (case-insensitive contains)
        products = Product.objects.filter(
            Q(name__icontains=query) | Q(category__icontains=query)
        ).order_by('created_at')
    else:
        products = Product.objects.all().order_by('created_at')

    return render(request, 'store/home.html', {'products': products, 'query': query})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    messages.success(request, "Product added to cart.")
    return redirect('cart')


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.price * quantity
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})


@require_POST
def update_cart(request, product_id):
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1

    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[str(product_id)] = quantity
    else:
        cart.pop(str(product_id), None)  # Remove if quantity 0 or less

    request.session['cart'] = cart
    return redirect('cart')


@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    order = Order.objects.create(user=request.user, complete=True)

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        OrderedItem.objects.create(order=order, product=product, quantity=quantity)

    request.session['cart'] = {}
    messages.success(request, f'Order #{order.id} placed successfully!')
    return render(request, 'store/checkout.html', {'order': order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')
    return render(request, 'store/order_history.html', {'orders': orders})


@login_required
def payment(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    # Calculate total amount
    amount = 0
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)

    for product in products:
        quantity = cart.get(str(product.id), 0)
        amount += product.price * quantity  # Assuming product.price is a Decimal

    if request.method == 'POST':
        # You might want to do payment processing here
        messages.success(request, "Payment processed successfully.")
        return redirect('checkout')

    return render(request, 'store/payment.html', {
        'amount': round(amount, 2),  # Pass the amount to the template
    })


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.is_cancellable():
        order.status = 'Cancelled'
        order.save()
        messages.success(request, f'Order #{order.id} has been cancelled.')
    else:
        messages.warning(request, f'Order #{order.id} cannot be cancelled.')

    return redirect('order-history')  # Make sure 'orders' matches your URL name for order history

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    reviews = product.reviews.all().order_by('-created_at')

    form = None
    if request.user.is_authenticated:
        review_exists = Review.objects.filter(product=product, user=request.user).exists()
        if not review_exists:
            if request.method == 'POST':
                form = ReviewForm(request.POST)
                if form.is_valid():
                    review = form.save(commit=False)
                    review.product = product
                    review.user = request.user
                    review.save()
                    return redirect('product-detail', product_id=product.id)
            else:
                form = ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'store/product_detail.html', context)

