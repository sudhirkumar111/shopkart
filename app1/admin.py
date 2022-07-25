from django.contrib import admin
from .models import Product, Category, Cart

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name','desc','price','img','category']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']

class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart, CartAdmin)