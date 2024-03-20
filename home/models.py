from django.db import models
from django.contrib.auth import get_user_model

import uuid

User = get_user_model()


class ProductModel(models.Model):
    uuid = models.UUIDField(max_length=190, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=4)
    description = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    colour = models.CharField(max_length=100)
    available_stock = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}  |  {self.price}"


class CategoryModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class DiscountModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='%(class)s_product')
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.product.name}  |  {self.discount_percentage}"


class ImageModel(models.Model):
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='%(class)s_product')
    image = models.ImageField()

    def __str__(self) -> str:
        return self.product.name


class ProductCategoryModel(models.Model):
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE, related_name='%(class)s_category')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='%(class)s_product')

    def __str__(self) -> str:
        return f"{self.product.name}  |  {self.category.name}"


class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_user')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='%(class)s_product')
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.user.uuid}  |  {self.product.name}"


class OrderModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_user')
    uuid = models.UUIDField(max_length=190, default=uuid.uuid4, editable=False, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=4)
    status = models.CharField(max_length=50, choices = (
        ("ordered", "Order Successful"),
        ("delivered", "Delivered Successfuly"),
    ))

    def __str__(self) -> str:
        return f"{self.uuid}  |  {self.status}"


class ReviewModel(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE, related_name='%(class)s_user')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='%(class)s_product')
    rating = models.IntegerField()
    review = models.TextField()

    def __str__(self) -> str:
        return f"{self.product.name}  |  {self.rating}"


class ProductOrderModel(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE, related_name='%(class)s_order')
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE, related_name='%(class)s_product')
    quantity = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.product.name}  |  {self.quantity}"