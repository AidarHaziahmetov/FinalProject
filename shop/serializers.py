from rest_framework import serializers
from shop import models

class CategorySerializer(serializers.ModelSerializer):
    count_products_in_category = serializers.SerializerMethodField()
    class Meta:
        model = models.Category
        fields = '__all__'

    def get_count_products_in_category(self, obj):
        return len(models.Product.objects.filter(category=obj))

class BrandSerializer(serializers.ModelSerializer):
    count_products_in_brand = serializers.SerializerMethodField()
    class Meta:
        model = models.Brand
        fields = '__all__'
    def get_count_products_in_brand(self, obj):
        return len(models.Product.objects.filter(brand=obj))

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    class Meta:
        model = models.Product
        fields = '__all__'

class User(serializers.ModelSerializer):
    user_profile = serializers.SerializerMethodField()
    class Meta:
        model = models.User
        fields = ['user_profile','username','email']


