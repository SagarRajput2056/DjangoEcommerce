from django.shortcuts import render, HttpResponse
from store.models import Product
# Create your views here.
def index(request):
    products = Product.objects.all()[0:6]

    return render(request, 'main/index.html',{
        'products': products
    })

def about(request):
    return render(request, 'main/about.html')