from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory, widgets
from django import forms

from shop import models
from shop.models import ProductCharacteristic, Product


class UserRegisterform(UserCreationForm):
    """
    Переопределенная форма регистрации пользователей
    """

    class Meta(UserCreationForm.Meta):
        model = models.User
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number')


class UpdateUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}

    class Meta:
        model = models.User
        fields = ['email', "phone_number"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['avatar']


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result



class ProductForm(forms.ModelForm):
    # category = forms.ModelMultipleChoiceField(
    #     queryset=models.Category.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,
    #     label='Категории',
    # )
    brand = forms.ModelChoiceField(
        queryset=models.Brand.objects.all(),
        label='Бренд',
    )
    # images = MultipleFileField(
    #     label="Добавить изображение",
    #     required=False,
    # )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        # self.fields['category'].widget.attrs = {}
        # self.fields['images'].widget = MultipleFileInput()
        # self.fields['images'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = models.Product
        fields = ['name','description','price','stock','image_preview']

    def save(self, commit=True):
        product = super().save()

        # Обработка изображений
        # images = self.cleaned_data.get('images')
        # if images:
        #     for image in images:
        #         models.ProductImage.objects.create(product=product, image=image)
        #
        # # Обработка удаления изображений
        # for i, image in enumerate(product.images.all()):
        #     delete_flag = self.cleaned_data.get(f'delete_image_{i}')
        #     if delete_flag:
        #         image.delete()

        # if commit:
        #     product.save()
        return product
# ProductCharacteristicForm = inlineformset_factory(Product, ProductCharacteristic, extra=1, fields=('name', 'value'))
