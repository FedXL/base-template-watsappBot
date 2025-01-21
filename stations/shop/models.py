from django.db import models
from clients.models import Client
from shop.utils import cart_buttons_generator


class Cart(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name="cart_related", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Cart {self.id} - {self.client}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.cart_items.all())



    def shopping_cart_buttons(self, language):
        items = self.cart_items.prefetch_related('product').all()
        summary_price = self.total_price
        buttons = cart_buttons_generator(items,summary_price, language)
        return buttons


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    product = models.ForeignKey('api_backend.ProductBlock', on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)
    @property
    def total_price(self):
        return self.quantity * self.product.price


    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def to_dict(self):
        return {
            "product": self.product.product_name,
            "product_header_kaz": self.product.header_kaz,
            "product_header_rus": self.product.header_rus,
            "quantity": self.quantity,
            "price": self.product.price,
            "total_price": self.total_price
        }

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[("pending", "Pending"), ("completed", "Completed"), ("canceled", "Canceled")], default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    @property
    def total_price(self):
        return sum(item.total_price for item in self.cart.cart_items.all())
    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.status}"