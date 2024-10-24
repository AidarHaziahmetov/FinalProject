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
from django.urls import path

from shop.views import BaseView, ProductListView, display_image, ProductDetailView, ProductListWithFilterView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', BaseView.as_view(), name='base'),
    path('product_list/', ProductListView.as_view(), name='product-list'),
    path("media/<path:path_to_image>", display_image, name="display-image"),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('', ProductListWithFilterView.as_view(), name='catalog'),
]
