import os

from PIL import Image
from django.conf import LazySettings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db.models import F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import TemplateView, ListView, DetailView, FormView, DeleteView, CreateView, UpdateView
from django_filters.views import FilterView
from rest_framework import viewsets
from rest_framework.utils import json

from shop import filters
from shop import forms
from shop import models
from shop import serializers

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
    model = models.Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = models.Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        object = super(ProductDetailView, self).get_object()
        context['product'] = object
        if self.request.user.is_authenticated:
            cart = models.Cart.objects.filter(user=self.request.user).first()
            context['cart_item'] = models.CartItem.objects.filter(product=object, cart=cart).first()
            print(context['cart_item'])
        return context


class ProductListWithFilterView(FilterView):
    model = models.Product
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


class CartView(LoginRequiredMixin, ListView):
    model = models.CartItem
    template_name = 'shop/cart.html'
    context_object_name = 'cart_items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_price"] = sum(cart_item.total_price for cart_item in context['cart_items'])
        return context

    def get_queryset(self):
        cart = models.Cart.objects.get_or_create(user=self.request.user)[0]
        return cart.cart_items.all().annotate(total_price=F('product__price') * F('quantity'))


class AddToCartView(LoginRequiredMixin, DetailView):
    model = models.Product
    template_name = 'shop/product_detail.html'

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        cart, created = models.Cart.objects.get_or_create(user=request.user)
        try:
            cart_item = cart.cart_items.get(product=product)
            cart_item.quantity += 1
            cart_item.save()
        except models.CartItem.DoesNotExist:
            cart_item = models.CartItem.objects.create(cart=cart, product=product)
        return redirect('product-detail', pk=product.pk)


class RemoveFromCartView(LoginRequiredMixin, DeleteView):
    model = models.CartItem
    context_object_name = 'cart_item'
    template_name = 'shop/cart_confirm_delete.html'
    success_url = reverse_lazy('cart')

    def get_success_url(self):
        return self.success_url


class UpdateCartQuantityView(LoginRequiredMixin, View):
    """
    View for updating the quantity of a product in the cart.
    """

    def post(self, request):
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = data.get('quantity')

            if not product_id or not quantity:
                return JsonResponse({'success': False, 'message': 'Некорректные данные'})

            product = models.Product.objects.get(pk=product_id)
            cart = models.Cart.objects.get(user=request.user)

            cart_item, created = models.CartItem.objects.get_or_create(
                cart=cart, product=product
            )

            # Validate quantity (crucial!)
            if quantity < 1 or quantity > product.stock:
                return JsonResponse({
                    'success': False,
                    'message': f"Неверное количество. Доступно {product.stock} шт."
                })

            cart_item.quantity = quantity
            cart_item.save()

            return JsonResponse({'success': True, 'message': 'Количество обновлено'})


        except (models.Product.DoesNotExist, models.Cart.DoesNotExist, ValueError):
            return JsonResponse({'success': False, 'message': 'Произошла ошибка'})


class CheckoutView(LoginRequiredMixin, CreateView):
    model = models.Order
    fields = []  # Нет полей для заполнения пользователем
    template_name = 'shop/checkout.html'
    success_url = reverse_lazy('order-success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = models.Cart.objects.filter(user=self.request.user).first()
        cart_items = cart.cart_items.all()

        context["cart_items"] = cart_items
        return context

    def form_valid(self, form):
        cart = models.Cart.objects.get_or_create(user=self.request.user)[0]
        cart_items = cart.cart_items.all()
        order = form.save(commit=False)
        order.user = self.request.user
        order.save()
        for cart_item in cart_items:
            product = cart_item.product
            product.stock -= cart_item.quantity
            product.save()
            models.OrderItem.objects.create(
                order=order,
                product=product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )
        cart.cart_items.all().delete()
        return super().form_valid(form)


class OrderSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'shop/order_success.html'


class OrderDetail(LoginRequiredMixin, DetailView):
    model = models.Order
    template_name = 'shop/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = super(OrderDetail, self).get_object()

        if object.user == self.request.user:
            context['order_items'] = object.order_items.all().annotate(total_price=F('product__price') * F('quantity'))
            context['total_price'] = object.get_total_price()
            return context
        else:
            return JsonResponse({'success': False, 'message': 'Чужие заказы смотреть не хорошо!'})


class ProductUpdateView(UpdateView):
    template_name = "shop/product_form.html"
    model = models.Product
    form_class = forms.ProductForm

    def form_valid(self, form):
        # Сохраняем изменения основного продукта
        response = super().form_valid(form)

        # Обрабатываем категории
        # categories = form.cleaned_data.get('category')
        # if categories:
        #     self.object.category.set(categories)

        # Обрабатываем бренд
        # brand = form.cleaned_data.get('brand')
        # if brand:
        #     self.object.brand = brand

        # Обрабатываем изображения
        # images = form.cleaned_data.get('images')
        # if images:
        #     for image in images:
        #         models.ProductImage.objects.create(product=self.object, image=image)
        #
        # # Обработка удаления изображений
        # for i, image in enumerate(self.object.images.all()):
        #     delete_flag = form.cleaned_data.get(f'delete_image_{i}')
        #     if delete_flag:
        #         image.delete()

        # Сохраняем изменения продукта
        # self.object.save()

        return response

    def get_success_url(self):
        if isinstance(self.object, models.Product):
            return reverse('product-detail', kwargs={'pk': self.object.pk})
        else:
            # Обрабатываем случай, когда self.object не является Product
            return reverse('product-list')



class ProductCreateView(CreateView):
    model = models.Product
    form_class = forms.ProductForm
    template_name = 'shop/product_form.html'  # Используем тот же шаблон
    success_url = reverse_lazy('product-list')  # Перенаправляем на список товаров

    def form_valid(self, form):
        # Сохраняем новый продукт
        # self.object = form.save()  # Сохраняем продукт

        # Обработка изображений
        # images = form.cleaned_data.get('images')
        # if images:
        #     for image in images.getlist('images'):
        #         models.ProductImage.objects.create(product=self.object, image=image)

                # Возвращаем ответ
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = models.Product
    success_url = reverse_lazy('product_list')
    template_name = 'shop/product_confirm_delete.html'  # Используйте шаблон подтверждения удаления

    def get_success_url(self):
        return reverse_lazy('catalog')


class CategoryAPI(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ProductAPI(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class BrandAPI(viewsets.ModelViewSet):
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer
