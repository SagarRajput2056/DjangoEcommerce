from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator
from store.models import Category, Product
# Create your views here.
def index(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 12)  # Show 12 products per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/index.html', {'page_obj': page_obj})

def about(request):
    return render(request, 'main/about.html')

def categories(request):
    categories = Category.objects.all()
    return render(request, 'main/categories.html',{
        'categories': categories
    })