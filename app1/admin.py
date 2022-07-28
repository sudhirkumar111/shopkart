from django.contrib import admin
from .models import Product, Category, Cart, ShippingDetail,OrderPlaced

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name','desc','price','img','category']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']

class CartAdmin(admin.ModelAdmin):
    list_display = ['id','user','product','quantity']


class ShippingAdmin(admin.ModelAdmin):
    list_display = ['id','user','fname','lname','city','contact','locality','pincode','state','landmark']


class OrderPlacedAdmin(admin.ModelAdmin):
    list_display = ['id','user','ship_add','product','quantity','ordered_date','status']

class OrderReturnAdmin(admin.ModelAdmin):
    list_display = ['id','user','ship_add','product','quantity','ordered_date','status']




admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(ShippingDetail, ShippingAdmin)
admin.site.register(OrderPlaced, OrderPlacedAdmin)