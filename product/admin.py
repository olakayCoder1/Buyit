from django.contrib import admin
from .models import (
    Company ,
    Product,
    ProductCategory
)
# Register your models here.


admin.site.register(Company)
admin.site.register(Product)
admin.site.register(ProductCategory)