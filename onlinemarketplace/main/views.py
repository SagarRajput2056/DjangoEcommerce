from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator
from store.models import Category, Product
# Create your views here.
def index(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 12)  # Show 12 products per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    payment_success = request.GET.get('payment_success', False)
    order_success = request.GET.get('order_success') == 'true'
    
    return render(request, 'main/index.html', {'page_obj': page_obj, 'payment_success': payment_success, 'order_success': order_success})

def about(request):
    return render(request, 'main/about.html')

def categories(request):
    categories = Category.objects.all()
    return render(request, 'main/categories.html',{
        'categories': categories
    })