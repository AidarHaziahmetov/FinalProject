from typing import Type

from django.conf import LazySettings
from django.contrib.admindocs.views import TemplateDetailView
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
import os
from PIL import Image
from django_filters.views import FilterView

from shop import filters
from shop.models import Product

settings = LazySettings()
# Create your views here.
class BaseView(TemplateView):
    template_name = 'base.html'

def display_image(request, path_to_image):
    """Отображает скачанное изображение."""

    try:
        full_image_path = os.path.join(settings.MEDIA_ROOT, *path_to_image.split('/'))
        image_data = Image.open(full_image_path)
        response: HttpResponse = HttpResponse(content_type="image/jpeg")
        image_data.save(response, format="JPEG")
        return response

    except FileNotFoundError:
        return HttpResponse("Изображение не найдено", status=404)
class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

class ProductListWithFilterView(FilterView):
    model = Product
    template_name = "shop/product_list_with_filter.html"
    context_object_name = "products"
    filterset_class = filters.ProductFilter