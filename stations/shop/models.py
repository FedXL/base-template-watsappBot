from django.db import models
from clients.models import Client
from shop.utils import cart_buttons_generator


class Cart(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE,
                                  related_name="cart_related",
                                  null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    spot = models.CharField(max_length=255, null=True, blank=True)
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
        return f"{self.quantity} x {self.product.product_name}"


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
    status = models.CharField(max_length=50, choices=[("pending", "pending"),
                                                      ("completed", "completed"),
                                                      ("canceled", "canceled")], default="pending")
    time_spot = models.CharField(default=None, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    @property
    def total_price(self):
        return sum(item.total_price for item in self.cart.cart_items.all())

    def __str__(self):
        return f"Order {self.id} - {self.client.username} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey('api_backend.ProductBlock', on_delete=models.DO_NOTHING)
    product_name = models.CharField(max_length=255,verbose_name='Название продукта')
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Стоимость в тенге')
    quantity = models.PositiveIntegerField(default=1,verbose_name='Количество')

    @property
    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} x {self.product_name}"

    def to_dict(self):
        return {
            "product": self.product_name,
            "quantity": self.quantity,
            "price": self.price,
            "total_price": self.total_price
        }