from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.ProductModel)
admin.site.register(models.ImageModel)
admin.site.register(models.OrderModel)
admin.site.register(models.ReviewModel)
admin.site.register(models.CartModel)
admin.site.register(models.CategoryModel)
admin.site.register(models.DiscountModel)