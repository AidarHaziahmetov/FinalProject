from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Администратор"),
        ("manager", "Менеджер"),
        ("customer", "Клиент"),
    )

    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default="customer", verbose_name="Роль"
    )
    phone_number = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ("username",)
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def is_admin(self):
        return self.role == "admin"

    def is_manager(self):
        return self.role == "manager"

    def is_customer(self):
        return self.role == "customer"

    def __str__(self) -> str:
        return super().__str__()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="profile_pics/", blank=True, null=True)

    class Meta:
        ordering = ("user",)
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def get_email(self):
        return self.user.email

    def __str__(self):
        return f'Профиль {self.user}'


# Create your models here.
class Category(models.Model):
    name = models.CharField(verbose_name="Название", max_length=255)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Родительская категория",
        related_name="children",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def get_all_children(self):
        children = []
        for category in Category.objects.filter(parent=self):
            children.append(category)
            children.extend(category.get_all_children())
        return children

    def __str__(self) -> str:
        return self.name


class Brand(models.Model):
    name = models.CharField(verbose_name="Название", max_length=255)
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )

    class Meta:
        ordering = ("name",)
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )
    image_preview = models.ImageField(upload_to='product_preview_images/', verbose_name="Превью", default="default.jpg",
                                      blank=True, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products", null=True, verbose_name="Бренд")
    category = models.ManyToManyField(
        Category,
        related_name="products",
        verbose_name="Категория",
        blank=False,
    )
    price = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Цена",
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="На складе")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated = models.DateTimeField(auto_now=True, verbose_name="Обновлен")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def is_in_stock(self):
        return self.stock > 0

    def __str__(self) -> str:
        return self.name + (" "+self.brand.name) if self.brand else ''


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", null=True, blank=False)
    image = models.ImageField(upload_to="product_images/", verbose_name="Фото")

    def __str__(self):
        return f"Изображение для {self.product.name}"

    class Meta:
        verbose_name = "Изображение товаров"
        verbose_name_plural = "Изображения товаров"


class ProductCharacteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='characteristics')
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Характеристика товара"
        verbose_name_plural = "Характеристики товара"

    def __str__(self):
        return f"{self.product.name}: {self.name}: {self.value}"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name="cart")

    class Meta:
        verbose_name = "Корзина пользователя"
        verbose_name_plural = "Корзины пользователей"

    def get_total_price(self):
        total = 0
        for item in self.cart_items.all():
            total += item.get_total_price()
        return total

    def __str__(self):
        return self.user.username


class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"

    def get_total_price(self):
        total = self.product.price * self.quantity
        return total


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=(
        ('pending', 'Ожидает подтверждения'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('completed', 'Завершен'),
    ), default='pending')

    def get_total_price(self):
        total = 0
        for item in self.order_items.all():
            total += item.get_total_price()
        return total

    def __str__(self):
        return f"Заказ #{self.id}"
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"Товар: {self.product.name}, Количество: {self.quantity}"
    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказов"
