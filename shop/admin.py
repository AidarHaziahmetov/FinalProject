from django.contrib import admin

from shop import models


# Register your models here.
@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "role")


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", 'price', 'stock')


@admin.register(models.ProductImage)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product",)

@admin.register(models.Brand)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.ProductCharacteristic)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "product")


@admin.register(models.CartItem)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("product", "cart")


@admin.register(models.Cart)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("user",)
