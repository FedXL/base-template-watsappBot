from django.db import models
from clients.models import Client

class Cart(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name="cart_related", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Cart {self.id} - {self.client}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.cart_items.all())

    def shopping_card_content(self):
        cart_items = self.cart_items.all()
        result = {}
        if not cart_items:
            return result
        for item in cart_items:
            result[item.product.product_name] = item.to_dict()
        result["total_price"] = self.total_price
        return result

    def shopping_card_buttons(self, language):
        buttons = {
                    "title": "Корзина",
                    "rows": [
                        {
                            "title": "Оформить заказ",
                            "value": "create_order",
                            "description": "Оформить заказ"
                        },
                        {
                            "title": "Очистить корзину",
                            "value": "clear_cart",
                            "description": "Очистить корзину"
                        }
                    ]
        }

        items = self.cart_items.prefetch_related('product').all()


        for item in items:
            product_name = item.product.header_rus if language == 'rus' else item.product.header_kaz
            buttons["rows"].append({
                "title": f"{product_name} - {item.quantity} шт.",
                "value": f"create_productblock_{item.product.product_name}",
                "description": f"{item.total_price} тг."
            })
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