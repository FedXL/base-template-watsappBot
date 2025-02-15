from typing import Any
from api_backend.models import ProductBlock
from clients.models import Client
from shop.models import CartItem, Cart





def collect_product_quantity_way(action:str,
                                 language:str,
                                 user_phone:str,
                                 text_data:str) -> tuple[bool, bool, str]:
    """
    Собирает количество товара в корзине
    quantity = collect_data_text_ice|cart_quantity
    """

    try:
        count_of_product = int(text_data)
    except ValueError:
        return False,False, 'Должно быть число'

    product = action.replace('collect_data_text_','').split('|')[0]
    product_obj = ProductBlock.objects.filter(product_name=product).first()

    if not product_obj:
        return False, False, f"Кривой продукт {product}"
    client = Client.objects.filter(phone=user_phone).first()
    if not client:
        return False,False,'Клиент не найден'
    cart = client.cart_related
    if not cart:
        cart = Cart.objects.create(client=client)
    cart_item_obj = CartItem.objects.filter(cart=cart, product=product_obj).first()
    if not cart_item_obj:
        cart_item_obj = CartItem.objects.create(cart=cart, product=product_obj, quantity=count_of_product)
    else:
        cart_item_obj.quantity = count_of_product
        cart_item_obj.save()

    what_next = f"create_productblock_{product_obj.product_name}"
    return product, what_next, product_obj.product_name



