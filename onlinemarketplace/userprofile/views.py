from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import UserProfile

# Create your views here.
def vendor_detail(request, pk):
    user = User.objects.get(pk=pk)

    return render(request, 'userprofile/vendor_detail.html', {
        'user': user
    })

def account_detail(request):
    return render(request, 'userprofile/account_detail.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            userprofile = UserProfile.objects.create(user=user)

            return redirect('index')
        
    else:
        form = UserCreationForm()
    
    return render(request, 'userprofile/register.html', {
        'form': form
    })