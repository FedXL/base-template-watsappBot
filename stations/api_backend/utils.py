from typing import Union, Literal, Tuple
from django.conf import settings
from api_backend.models import InfoBlock, Variables, ProductBlock
from clients.models import Client


def infoblock_serializer(infoblock_name, language, for_operator_link = False)-> tuple:
    infoblock_obj = InfoBlock.objects.filter(name=infoblock_name).first()

    if not infoblock_obj:
        return False, False

    infoblock_block = infoblock_obj.block_to_dict(language)
    menu = infoblock_obj.info_button_reverse.menu
    create_menu_text = 'create_menu_' + menu.name
    if language == 'rus':

        operator = Variables.objects.filter(name='operator').first().rus
        comeback = Variables.objects.filter(name='comeback').first().rus

    else:

        operator = Variables.objects.filter(name='operator').first().kaz
        comeback = Variables.objects.filter(name='comeback').first().kaz

    if for_operator_link:
        buttons = [
            {
                "title": comeback,
                "value": create_menu_text
            }
        ]
    else:
        buttons = [
            {
                "title": operator,
                "value": f"create_operator_link_from_{infoblock_name}"
            },
            {
                "title": comeback,
                "value": create_menu_text
            }
        ]
    return infoblock_block ,buttons



def client_cart_serializer(client):
    """Сериализация корзины клиента"""
    result_dict = {}
    assert isinstance(client, Client), "client must be an instance of Client"
    cart = client.cart_related
    items = cart.cart_items.all()
    if not items:
        return False
    for item in items:
        item_dict = item.to_dict()
        result_dict[item.product.product_name] = item_dict
    return result_dict


def create_product_block_data(action,
                              language: Literal['rus','kaz'],
                              user_phone:str,
                              result_data) -> Tuple[bool, Union[str, dict]]:

    client = Client.objects.filter(phone=user_phone).first()
    if not client:
        return False, 'Client not found!'

    cart_dict = client_cart_serializer(client)

    product_block_result = {}
    product_name = result_data.get('product_name', None)

    if cart_dict:
        product_data = cart_dict.get(product_name, None)
    else:
        product_data = None
    product_block = ProductBlock.objects.filter(product_name=product_name).first()
    if not product_block:
        return False,'Product not found!'
    product_block_dict = product_block.block_to_dict(language)
    try:
        if language == 'rus':
            go_to_card_text = Variables.objects.filter(name='cart').first().rus
        elif language == 'kaz':
            go_to_card_text = Variables.objects.filter(name='cart').first().kaz
    except:
        go_to_card_text = 'CART'

    product_block_result['infoblock_block'] = product_block_dict

    buttons = [{
        "title": "collect quantity",
        "value": f"collectquantity_{product_name}"
    }, {
        "title": go_to_card_text,
        "value": f"create_special_menu_cart",
    }, {
        "title": "comeback to menu",
        "value": f"create_menu_main"
    }]

    body = product_block_result['infoblock_block']['body']
    if product_data:
        summary = int(product_data.get('total_price')) * int(product_data.get('quantity'))
        body = body + f"Стоимость {product_data.get('price')} Х {product_data.get('quantity')} = {summary} ₸."
    else:
        body = body + f"Стоимость 0 Х 0 = 0 ₸."

    product_block_result['infoblock_block']['body'] = body
    product_block_result['buttons'] = buttons
    url = settings.HOST_PREFIX + product_block.photo.url
    product_block_result['image_url'] = url
    result_data['infoblock'] = product_block_result

    return True, result_data