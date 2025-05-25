import base64
import json
import uuid
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from .models import Category, Product, Order, OrderItem
from .cart import Cart
from .forms import OrderForm
# Create your views here.


from django.db.models import Count

def recommend_products(user, exclude_product_id=None, current_product=None, limit=5):
    # If a current product is passed (e.g., on a product detail page)
    if current_product:
        category = current_product.category  # Get the category of the current product
        
        # Get IDs of previously purchased products within the same category (clothes, for example)
        purchased_product_ids = OrderItem.objects.filter(order__created_by=user)\
                                                 .filter(product__category=category)\
                                                 .values_list('product_id', flat=True)

        # Get recommended products in the same category, excluding the current product and previously bought items
        recommended_products = Product.objects.filter(category=category)\
                                               .exclude(id=exclude_product_id)\
                                               .exclude(id__in=purchased_product_ids)\
                                               .distinct()[:limit]
    else:
        # Default behavior for products from top categories the user has bought from
        category_ids = OrderItem.objects.filter(order__created_by=user)\
                                         .values('product__category')\
                                         .annotate(total=Count('product__category'))\
                                         .order_by('-total')\
                                         .values_list('product__category', flat=True)[:3]

        purchased_product_ids = OrderItem.objects.filter(order__created_by=user)\
                                                 .values_list('product_id', flat=True)

        recommended_products = Product.objects.filter(category_id__in=category_ids)\
                                               .exclude(id__in=purchased_product_ids)\
                                               .exclude(id=exclude_product_id)\
                                               .distinct()[:limit]

    return recommended_products


from django.http import JsonResponse

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if stock is available
    if product.stock <= 0:
        return JsonResponse({'error': 'Out of stock'}, status=400)

    cart = Cart(request)
    cart.add(product_id)

    return redirect('index')

def change_quantity(request, product_id):
    action = request.GET.get('action', '')

    if action in ['increase', 'decrease']:
        quantity = 1 if action == 'increase' else -1

        cart = Cart(request)
        cart.add(product_id, quantity, True)

    return redirect('cart_view')


def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)

    return redirect('cart_view')

def cart_view(request):
    cart = Cart(request)
    return render(request,'store/cart_view.html',{
        'cart': cart
    })

@login_required
def checkout(request):
    cart = Cart(request)
    user = request.user

    initial_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    }

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            total_price = 0
            payment_method = form.cleaned_data['payment_method']
            
            for item in cart:
                total_price += item['product'].price * item['quantity']
                product = item['product']
                if product.stock < item['quantity']:  # If stock is less than cart quantity
                    messages.error(request, f"Not enough stock for {product.title}.")
                    return redirect('cart_view')  # Redirect to cart if stock is insufficient
                product.stock -= item['quantity']  # Reduce stock
                product.save()
            
            order = form.save(commit=False)
            order.created_by = request.user
            order.paid_amount = total_price
            order.payment_method = payment_method
            order.is_paid = False
            order.save()
            
            for item in cart:
                product = item['product']
                quantity = item['quantity']
                price = product.price * quantity
                OrderItem.objects.create(order=order, product=product, price=price, quantity=quantity)
            
            if payment_method == 'Esewa':
                return render(request, "store/esewacheckout.html", {'order': order})
            else:
                cart.clear()
                return redirect(f"/?order_success=true")
    else:
        form = OrderForm(initial=initial_data)
 
    return render(request, 'store/checkout.html', {
        'cart': cart,
        'form': form,
    })


def payment_confirmation(request, product_id:str):
    product_id = product_id.replace("-", "")
    encoded_data = request.GET.get('data')
    if encoded_data:
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        payment_data = json.loads(decoded_data)
        
        if payment_data['status'] == 'COMPLETE':
            order = Order.objects.get(transaction_uuid=product_id)
            order.is_paid = True
            order.save()

            cart = Cart(request)
            cart.clear()

            return redirect(f"/?payment_success=true")
        else:
            messages.error(request, 'Payment failed. Please try again.')

        return redirect('index')

def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))

    return render(request, 'store/search.html',{
        'query': query,
        'products': products
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()

    return render(request, 'store/category_detail.html', {
        'category': category,
        'products': products
    })

def product_detail(request, category_slug, slug):
    product = get_object_or_404(Product, slug=slug)

    # Ensure the recommendations consider the current product's category and exclude purchased items
    recommendations = recommend_products(request.user, exclude_product_id=product.id, current_product=product) if request.user.is_authenticated else []

    return render(request, 'store/product_detail.html', {
        'product': product,
        'recommendations': recommendations
    })



