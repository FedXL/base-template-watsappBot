from django.db import transaction

from clients.models import Client
from shop.models import Order, OrderItem


def create_order(phone:str,my_logger) -> bool:
    """
    Create order for client with phone number
    """
    try:
        with transaction.atomic():
            client = Client.objects.filter(phone=phone).first()
            if not client:
                return False
            cart = client.cart_related
            items = cart.cart_items.all()
            order = Order.objects.create(client=client,time_spot=cart.time_spot)
            for item in items:
                order_item = OrderItem.objects.create(order=order,
                                                      product=item.product,
                                                      product_name=item.product.product_name,
                                                      quantity=item.quantity)
        return True
    except Exception as e:
        my_logger.info(f"Error in create_order: {e}")
        return False


def create_order_texts(language):
    if language == 'rus':
        header =