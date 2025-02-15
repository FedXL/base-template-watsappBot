from django.contrib import admin
from shop.models import Order, Cart, CartItem


class OrderItemInline(admin.TabularInline):
    model = CartItem
    extra = 0



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Order._meta.fields]

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Cart._meta.fields]
    inlines = [OrderItemInline]