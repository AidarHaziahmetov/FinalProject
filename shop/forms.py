from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory

from shop import models
from shop.models import ProductCharacteristic, Product


class UserRegisterForm(UserCreationForm):
    """
    Переопределенная форма регистрации пользователей
    """

    class Meta(UserCreationForm.Meta):
        model = models.User
        fields = UserCreationForm.Meta.fields + ('email',)

ProductCharacteristicForm = inlineformset_factory(Product, ProductCharacteristic, extra=1, fields=('name', 'value'))