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
        fields = ['email',"phone_number"]
class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['avatar']


class ProductForm(forms.ModelForm):
    category = forms.ModelMultipleChoiceField(
        queryset=models.Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Категории',
    )
    brand = forms.ModelChoiceField(
        queryset=models.Brand.objects.all(),
        label='Бренд',
    )
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'brand': forms.Select(attrs={'class': 'form-control'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs = {'class': 'form-control'}
        self.fields['category'].widget.attrs = {}


# ProductCharacteristicForm = inlineformset_factory(Product, ProductCharacteristic, extra=1, fields=('name', 'value'))