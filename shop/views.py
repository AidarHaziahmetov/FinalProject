from django.conf import LazySettings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View

from django.views.generic import TemplateView, ListView, DetailView, FormView
import os
from PIL import Image
from django_filters.views import FilterView

from shop import filters
from shop import forms
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


class RegisterView(FormView):
    form_class = forms.UserRegisterform
    template_name = "registration/register.html"


    def form_valid(self, form):
        result = super().form_valid(form)
        if result.status_code == 302:
            form.save()
        return result

    def get_success_url(self):
        return reverse_lazy('catalog')


class MyLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy('catalog')


@login_required
def profile(request):
    return render(request, "shop/profile.html")

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        profile = user.profile
        user_form = forms.UpdateUserForm(instance=user)
        profile_form = forms.ProfileForm(instance=profile)
        context = {'user': user, 'profile': profile, 'user_form': user_form, 'profile_form': profile_form}
        return render(request, 'shop/profile.html', context)

    def post(self, request):
        user = request.user
        profile = user.profile
        user_form = forms.UpdateUserForm(request.POST, instance=user)
        profile_form = forms.ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
        else:
            context = {'user': user, 'profile': profile, 'user_form': user_form, 'profile_form': profile_form}
            return render(request, 'shop/profile.html', context)
