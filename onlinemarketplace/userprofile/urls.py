from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('account/', views.account_detail, name='account_detail'),
    path('my-store/', views.my_store, name='my_store'),
    path('my-store/add-product/', views.add_product, name='add_product'),
    path('my-store/edit-product/<int:pk>/', views.edit_product, name='edit_product'),
    path('vendors/<int:pk>/', views.vendor_detail, name='vendor_detail'),
]