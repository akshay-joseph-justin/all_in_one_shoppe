from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.ProductModel)
admin.site.register(models.OrderModel)
admin.site.register(models.CartModel)
admin.site.register(models.CategoryModel)
admin.site.register(models.ImageModel)
admin.site.register(models.CartProductModel)
admin.site.register(models.OrderProductModel)
admin.site.register(models.PolicyModel)
admin.site.register(models.BannerModel)
