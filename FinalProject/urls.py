"""
URL configuration for FinalProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path, include

from shop.views import BaseView, ProductListView, display_image, ProductDetailView, ProductListWithFilterView, \
    RegisterView, MyLoginView, profile

urlpatterns = [

    path('admin/', admin.site.urls, name='admin'),
    path('base/', BaseView.as_view(), name='base'),
    path('product_list/', ProductListView.as_view(), name='product-list'),
    path("media/<path:path_to_image>", display_image, name="display-image"),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('', ProductListWithFilterView.as_view(), name='catalog'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path('login/', MyLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path("profile/", profile, name="profile"),
]
