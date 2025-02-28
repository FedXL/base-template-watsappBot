from django.db import transaction

from api_backend.replies import replies_text, R, SupportLogic
from clients.models import Client
from shop.models import Order, OrderItem


def create_order(phone:str,my_logger) -> bool:
    """
    Create order for client with phone number
    """
    my_logger.info(f"START create_order: {phone}")
    try:
        with transaction.atomic():
            my_logger.info(f"Try to find client by phone: {phone}")
            client = Client.objects.filter(phone=phone).first()
            if not client:
                return False
            my_logger.info(f"Client found: {client}")
            my_logger.info(f"Try to find cart for client: {client}")
            cart = client.cart_related
            if not cart:
                my_logger.info(f"Cart not found")
                return False
            my_logger.info(f"Cart found: {cart}")
            my_logger.info(f"Try to get items")
            items = cart.cart_items.all()
            if not items:
                my_logger.info(f"Items not found")
                return False
            my_logger.info(f"Items found: {items}")
            my_logger.info(f"Try to create order")
            order = Order.objects.create(client=client,
                                         time_spot=cart.spot)
            my_logger.info(f"Order created: {order}")
            for item in items:
                my_logger.info(f"Try to create order item: {item}")
                order_item = OrderItem.objects.create(order=order,
                                                      product=item.product,
                                                      product_name=item.product.product_name,
                                                      quantity=item.quantity,
                                                      price=item.product.price)
                my_logger.info(f"Order item created: {order_item}")
        with transaction.atomic():
            my_logger.info(f"Try to delete cart")
            items = cart.cart_items.all()
            items.delete()
            my_logger.info(f"Cart deleted")
        return True
    except Exception as e:
        my_logger.info(f"Error in create_order: {e}")
        return False


def create_text_success(language, is_success):
    """Отчет о заказе"""
    result  = {}
    if is_success:

        data = {
            "header": replies_text(R.Order.SUCCESS_HEADER, language),
            "body": replies_text(R.Order.SUCCESS_BODY,language=language),
            "footer": replies_text(R.Order.SUCCESS_BODY,language=language)
        }
    else:
        data = {
            "header": replies_text(R.Order.FAIL_HEADER, language),
            "body": replies_text(R.Order.FAIL_BODY,language=language),
            "footer": replies_text(R.Order.FAIL_FOOTER,language=language)
        }

    result['infoblock'] = {"infoblock_block": data,
                           "buttons": [
                               {
                                   "title": replies_text(R.Navigate.COMEBACK, language),
                                   "value": "create_special_menu_cart"
                               }
                           ]}

    result['support_logic'] = SupportLogic.WITH_BUTTONS
    result['what_next'] = 'button_message'
    return result