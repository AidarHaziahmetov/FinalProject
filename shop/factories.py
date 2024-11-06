import factory
from factory.django import ImageField
from shop import models


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    class Meta:
        model = models.Category

class BrandFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    description = factory.Faker('text')
    class Meta:
        model = models.Brand

class ImagesFactory(factory.django.DjangoModelFactory):
    product = factory.SubFactory('shop.factories.ProductFactory', images=None)
    image = ImageField()
    class Meta:
        model = models.ProductImage


class ProductFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('name')
    description = factory.Faker('text')
    image_preview = ImageField()
    brand = factory.SubFactory(BrandFactory)
    category = factory.RelatedFactory(CategoryFactory)
    images = factory.RelatedFactory(ImagesFactory)
    price = factory.Faker('random_int')
    stock = factory.Faker('random_int')
    created = factory.Faker('date_time')
    updated = factory.Faker('date_time')

    class Meta:
        model = models.Product