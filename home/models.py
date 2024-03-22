import os
import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

User = get_user_model()


class CategoryModel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self) -> str:
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


def product_image_upload_path(model, filename):
    return os.path.join("uploads", model.name, filename)


def image_upload_path(model, filename):
    return os.path.join("uploads", model.product.name, filename)


class ProductModel(models.Model):
    uuid = models.UUIDField(max_length=190, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    colour = models.CharField(max_length=100)
    image = models.ImageField(upload_to=product_image_upload_path)
    available_stock = models.CharField(max_length=100)
    slug = models.SlugField()

    def __str__(self):
        return f"{self.name}  |  {self.price}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ImageModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_path)

    def __str__(self):
        return f"{self.product.name}"


class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_user')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='%(class)s_product')
    quantity = models.IntegerField()
    slug = models.SlugField(null=True)

    def __str__(self) -> str:
        return f"{self.user.uuid}  |  {self.product.name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product.name)
        super().save(*args, **kwargs)


class OrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_user')
    uuid = models.UUIDField(max_length=190, default=uuid.uuid4, editable=False, unique=True)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='%(class)s_product')
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=150)
    status = models.CharField(max_length=50,
                              choices=(("ordered", "Order Successful"), ("delivered", "Delivered Successfully"),))

    def __str__(self) -> str:
        return f"{self.uuid}  |  {self.status}"


class ReviewModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_user')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='%(class)s_product')
    rating = models.IntegerField()
    review = models.TextField()

    def __str__(self) -> str:
        return f"{self.product.name}  |  {self.rating}"
