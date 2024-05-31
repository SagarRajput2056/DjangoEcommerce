from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from django.contrib import messages
from django.core.paginator import Paginator

from userprofile.forms import CustomUserCreationForm
from store.models import Order, Product, OrderItem

from .models import UserProfile
from store.forms import ProductForm

# Create your views here.
def vendor_detail(request, pk):
    user = User.objects.get(pk=pk)

    return render(request, 'userprofile/vendor_detail.html', {
        'user': user
    })

@login_required
def my_store(request):
    order_items = OrderItem.objects.filter(product__user=request.user).order_by('-order__created_at')
    paginator = Paginator(order_items, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'userprofile/my_store.html', {
        'page_obj': page_obj,  
    })

    
def toggle_order_status(request, order_id):
    order = Order.objects.get(id=order_id)
    if order.is_paid:
        return redirect('my_store')   
    order.is_paid = not order.is_paid 
    order.save()
    return redirect('my_store')  

@login_required
def store_order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    return render(request,'userprofile/store_order_detail.html',{
        'order': order,
    })

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            title = request.POST.get('title')
            product = form.save(commit=False)
            product.user = request.user
            product.slug = slugify(title)
            product.save()
            messages.success(request, 'The product was added!')
            return redirect('my_store')
    else:
            form = ProductForm()

    return render(request, 'userprofile/product_form.html',{
        'title': 'Add Product',
        'form': form,
    })

@login_required
def edit_product(request, pk):
    
    product = Product.objects.filter(user=request.user).get(pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'The changes were saved!')
            return redirect('my_store')
    
    else:
        form = ProductForm(instance=product)

    return render(request, 'userprofile/product_form.html',{
        'title': 'Edit Product',
        'product': product,
        'form': form,
    })

@login_required
def delete_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    product.delete()
    messages.success(request, 'The product was deleted!')
    return redirect('my_store')

@login_required
def account_detail(request):
    return render(request, 'userprofile/account_detail.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            print("User created:", user)
            print("UserProfile created:", user.userprofile)
            return redirect('index')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'userprofile/register.html', {
        'form': form
    })