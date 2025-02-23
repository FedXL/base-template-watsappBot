
from api_backend.replies import R, replies_text, SupportLogic, WATER_19L_BOTTLE
from clients.models import Client
from django.utils.timezone import now
from datetime import timedelta, datetime
from shop.models import Cart




"""
шпаргалка по меню 
{
    "what_next": "create_menu_main",
	"menu": {
		"menu_block": {
			"header": "Главное меню",
			"body": "Теперь можно приступить к покупкам.",
			"footer": "используйте кнопки",
			"list_title": "товары",
			"section_title": "товары"
		},
		"menu_buttons": [
			{
				"title": "товары",
				"rows": [
					{
						"title": "Вода",
						"description": "проследуйте для просмотра товаров",
						"value": "create_menu_water_menu"
					},
				]
			}
		]
	}
}
"""



def no_buttons_address_block(language):
    header = replies_text(R.AskBlock.ADDRESS_HEADER, language)
    infoblock = {
        "header": header,
        "body": "",
        "footer": ""
    }
    return {'infoblock': {'infoblock_block': infoblock},
            'support_logic': SupportLogic.NO_BUTTONS,
            'what_next': 'datacollector|catch_address'}



def with_buttons_address_block(language, address):

    header = replies_text(R.AskBlock.ADDRESS_HEADER, language)
    body = replies_text(R.AskBlock.ADDRESS_BODY, language)
    body += f"\n{address}"
    footer = replies_text(R.AskBlock.ADDRESS_FOOTER, language)

    confirm_button = replies_text(R.AskBlock.Buttons.CONFIRM, language)
    change_button = replies_text(R.AskBlock.Buttons.CHANGE, language)


    buttons = [
        {
            "title": confirm_button,
            "value": "address_confirmed"
        },
        {
            "title": change_button,
            "value": "change_address"
        }
    ]


    info_block = {
        "header": header,
        "body": body,
        "footer": footer,
        "buttons": buttons
    }

    result = {
            'infoblock': {
                            'infoblock_block': info_block,
                             'buttons': buttons
                            },
            'support_logic': SupportLogic.WITH_BUTTONS,
            'what_next': 'datacollector|catch_address'
        }
    return result





def get_delivery_slots(language):
    """
    В телеге бот работает по принципу:  если заявку подают до 13:00
    то она падает на доставку на этот же день, с 15:00 до 20:00.
    Если после 20:00 заявка то на доставку встает с 9:00 до 15:00 следующего дня
    [
  {
    "title": "Section 1",
    "rows": [
      {
        "title": "Row 1",
        "value": "row-1",
        "description": "the first row"
      },
      {
        "title": "Row 2",
        "value": "row-2",
        "description": "the 2nd row"
      }
    ]
  }
]
    """
    buttons = [
        {
            "title": replies_text(R.AskBlock.SPOT_TITLE, language),
            "rows": [],
        }
    ]
    tomorrow_after = now()
    rows = []

    if tomorrow_after.hour <= 13:
        rows.append(
            {
                "title": replies_text(R.AskBlock.TOMORROW_15_20,language),
                "value": "datacollector|catch_time|today_15_20",
                "description": f"{tomorrow_after.day}.{tomorrow_after.month}.{tomorrow_after.year} с 15:00 до 20:00"}
        )
        tomorrow_after = tomorrow_after + timedelta(days=1)

    rows.append(
        {
            "title": replies_text(R.AskBlock.TOMORROW_9_15, language),
            "value": "datacollector|catch_time|tomorrow_9_15",
            "description": f"{tomorrow_after.day}.{tomorrow_after.month}.{tomorrow_after.year} с 9:00 до 15:00"
        }
    )
    rows.append(
        {
            "title": replies_text(R.AskBlock.TOMORROW_15_20, language),
            "value": "datacollector|catch_time|tomorrow_15_20",
            "description": f"{tomorrow_after.day}.{tomorrow_after.month}.{tomorrow_after.year} с 15:00 до 20:00"
        }
    )
    tomorrow_after = tomorrow_after + timedelta(days=1)

    rows.append(
        {
            "title": replies_text(R.AskBlock.AFTER_TOMORROW_9_15, language),
            "value": "datacollector|catch_time|after_tomorrow_9_15",
            "description": f"{tomorrow_after.day}.{tomorrow_after.month}.{tomorrow_after.year} с 9:00 до 15:00"
        }
    )
    rows.append(
        {
            "title": replies_text(R.AskBlock.AFTER_TOMORROW_15_20, language),
            "value": "datacollector|catch_time|after_tomorrow_15_20",
            "description": f"{tomorrow_after.day}.{tomorrow_after.month}.{tomorrow_after.year} с 15:00 до 20:00"
        }
    )
    buttons[0]['rows'] = rows
    return buttons


def create_time_block(language):
    menu = {}

    menu_block = {
        "header": replies_text(R.AskBlock.SPOT_HEADER, language),
        "body": replies_text(R.AskBlock.SPOT_BODY, language),
        "footer": replies_text(R.AskBlock.SPOT_FOOTER, language),
        "list_title": replies_text(R.AskBlock.SPOT_TITLE, language),
        "section_title": replies_text(R.AskBlock.SPOT_SECTION, language)
    }

    buttons = get_delivery_slots(language)
    menu['menu_block'] = menu_block
    menu['menu_buttons'] = buttons
    return menu


def how_many_bootle_you_need(cart:Cart):
    items = cart.cart_items.all()
    for item in items:
        product_name = item.product.product_name
        if product_name == WATER_19L_BOTTLE:
            quantity = item.quantity
            if quantity:
                return quantity
            else:
                raise ValueError("Хрень какая то иди разбирайся в how_many_bootle_you_need")
    return False


def collect_data_before_order(the_way,
                              language,
                              user_phone,
                              what_next_comment=None,
                              what_next_details=None,
                              parsing_variable=None,
                              my_logger=None
                              ) -> dict:
    """
    the_way = catch_address (action=datacollecter|catch_address)
    what_next_comment = сообщение об ошибке
    what_next_details = содержимое
    """
    my_logger.info(f"START collect_data_before_order: {the_way}")
    result = {}
    client = Client.objects.filter(phone=user_phone).first()
    if not client:
        return {"error": "Клиент не найден"}

    match the_way:
        case "ask_address":
            """Спросить адрес"""
            address = client.address
            if address:
                my_logger.info(f"Спросить адрес с кнопками")
                result = with_buttons_address_block(language, address)
            else:
                my_logger.info(f"Спросить адрес без кнопок {user_phone}")
                result = no_buttons_address_block(language)



        case "catch_address":
            my_logger.info(f'start CATCH ADDRESS {what_next_details}')
            """Поймать адрес -> опрос тайм слота"""
            if what_next_details:
                the_way_2 = what_next_details
                if the_way_2 == 'change_address':
                    my_logger.info('CATCH ADDRESS: change_address')
                    result = no_buttons_address_block(language)

                    client.address = None
                    client.save()
                elif the_way_2 == 'address_confirmed':
                    my_logger.info('CATCH ADDRESS: address_confirmed')
                    result['menu'] = create_time_block(language)
                    result['what_next'] = 'create_menu'
                else:
                    my_logger.info(f'CATCH ADDRESS: {what_next_details}')

                    client.address = what_next_details
                    client.save()
                    result['menu'] = create_time_block(language)
                    result['what_next'] = 'create_menu'
            else:
                raise ValueError("Что то пошло не так в catch_address")


        case "address_confirmed":
            """у нас подтвержденный адрес -> опрос тайм слота"""
            my_logger.info("Подтвержденный адрес затем тайм слот")
            result['menu'] = create_time_block(language)
            result['what_next'] = 'create_menu'

        case "catch_time":
            my_logger.info('start CATCH TIME')
            """Поймать время доставки и задать вопрос про  [тару <-> Подтвердить - создать заказ]"""
            time = parsing_variable
            cart = client.cart_related
            cart.time_spot = time
            cart.save()

            result['what_next'] = 'create_infoblock'
            how_many_19L_bootle = how_many_bootle_you_need(cart=cart)
            my_logger.info(f"how_many_19L_bootle: {how_many_19L_bootle}")
            if how_many_19L_bootle:
                """Задаем вопрос про бутылки"""
                body = replies_text(R.AskBlock.CONTAINER_BODY, language)
                body = body.replace('bottle', str(how_many_19L_bootle))
                infoblock_data = {
                    "header": replies_text(R.AskBlock.CONTAINER_HEADER, language),
                    "body": body,
                    "footer": replies_text(R.AskBlock.CONTAINER_FOOTER, language),

                }
                result['infoblock'] = {"infoblock_block": infoblock_data,
                                       "buttons": [
                        {
                            "title": replies_text(R.Navigate.YES, language),
                            "value": "create_order"
                        },
                        {
                            "title": replies_text(R.Navigate.NO, language),
                            "value": "create_special_menu_cart"
                        }
                    ]}
            else:
                """create_order"""
                result['what_next'] = 'create_order'

    return result













