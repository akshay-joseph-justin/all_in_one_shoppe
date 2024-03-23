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
    slug = models.SlugField(null=True)

    def __str__(self) -> str:
        return f"{self.user.uuid}  |  {self.user.username}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)


class OrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_user')
    uuid = models.UUIDField(max_length=190, default=uuid.uuid4, editable=False, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=150)
    status = models.CharField(max_length=50,
                choices=(("created", "order created"),("ordered", "Order Successful"), ("delivered", "Delivered Successfully"),))
    slug = models.SlugField(null=True)

    def __str__(self) -> str:
        return f"{self.uuid}  |  {self.status}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.uuid)
        super().save(*args, **kwargs)


class CartProductModel(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, related_name='%(class)s_cart')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='%(class)s_product')
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.cart.user.username}  |  {self.product.name}"


class OrderProductModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='%(class)s_order')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='%(class)s_product')
    quantity = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.order.uuid}  |  {self.product.name}"


class ReviewModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_user')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='%(class)s_product')
    rating = models.IntegerField()
    review = models.TextField()

    def __str__(self) -> str:
        return f"{self.product.name}  |  {self.rating}"
