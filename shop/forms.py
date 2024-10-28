from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
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
        fields = ['email',"phone_number"]
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
            result = single_file_clean(data, initial)
        return result

class BrandForm(forms.ModelForm):
    class Meta:
        model = models.Brand
        fields = ['name']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}

class CategoryForm(forms.ModelForm):
    class Meta:
        model = models.Category
        fields = ['name']

class ProductForm(forms.ModelForm):
    images = MultipleFileField(label='Изображения')
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'brand': forms.Select(attrs={'class': 'form-control'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].queryset = models.Brand.objects.all()
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}

        self.fields['images'].widget = MultipleFileInput()

    def save(self, commit=True):
        product = super().save(commit=False)
        product.save()

        if commit:
            if self.cleaned_data['images']:
                for image in self.cleaned_data['images']:
                    product_image = models.ProductImage.objects.create(image=image)
                    product.images.add(product_image)
            if self.cleaned_data['categories']:
                for category in self.cleaned_data['categories']:
                    product.categories.add(category)
            if self.cleaned_data.get('characteristics'):
                for characteristic in self.cleaned_data['characteristics']:
                    ProductCharacteristic.objects.create(
                        product=product,
                        name=characteristic['name'],
                        value=characteristic['value'],
                    )
        return product

    def clean_characteristics(self):
        characteristics = self.cleaned_data.get('characteristics')
        if characteristics:
            characteristics = characteristics.split(';')
            characteristics_list = []
            for characteristic in characteristics:
                parts = characteristic.strip().split(':')
                if len(parts) == 2:
                    name, value = parts
                    characteristics_list.append({
                        'name': name.strip(),
                        'value': value.strip(),
                    })
                else:
                    raise forms.ValidationError('Неверный формат характеристики. Должно быть "Название: Значение".')
            return characteristics_list
        return []


# ProductCharacteristicForm = inlineformset_factory(Product, ProductCharacteristic, extra=1, fields=('name', 'value'))