from typing import Any
from api_backend.models import ProductBlock
from api_backend.replies import replies_text, R
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
        return False,False, replies_text(R.Quantity.SHOULD_BE_INT, language)

    product = action.replace('collect_data_text_','').split('|')[0]
    product_obj = ProductBlock.objects.filter(product_name=product).first()



    if not product_obj:
        return False, False, f"Кривой продукт {product}"

    if product in ["water_10L","water_5L"]:
        if product == "water_10L" and count_of_product < 5:
            return False,False, replies_text(R.Quantity.SHOULD_BE_MORE_5, language)
        elif product == 'water_5L' and count_of_product < 10:
            return False, False, replies_text(R.Quantity.SHOULD_BE_MORE_10, language)
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



