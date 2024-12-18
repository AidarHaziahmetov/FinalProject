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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from shop import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('categories', views.CategoryAPI, basename='categories')
router.register('products', views.ProductAPI, basename='products')
router.register('brands', views.BrandAPI, basename='brands')
urlpatterns = [

    path('admin/', admin.site.urls, name='admin'),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
    path('product_list/', views.ProductListView.as_view(), name='product-list'),
    # path('product_create/', views.ProductCreateView.as_view(), name='product-list'),
    path("media/<path:path_to_image>", views.display_image, name="display-image"),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('product/create', views.ProductCreateView.as_view(), name='product-create'),
    path('product/<int:pk>/update', views.ProductUpdateView.as_view(), name='product-update'),
    path('', views.ProductListWithFilterView.as_view(), name='catalog'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path('add_to_cart/<int:pk>/', views.AddToCartView.as_view(), name='add-to-cart'),
    path('remove_from_cart/<int:pk>/', views.RemoveFromCartView.as_view(), name='remove-from-cart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('update_cart_quantity/', views.UpdateCartQuantityView.as_view(), name='update-cart-quantity'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('order_success/', views.OrderSuccessView.as_view(), name='order-success'),
    path('order_detail/<int:pk>/', views.OrderDetail.as_view(), name='order-detail'),
    path('product/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),

] + router.urls
