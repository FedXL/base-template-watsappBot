import logging
from api_backend.replies import R, replies_text, SupportLogic
from clients.models import Client
from django.utils.timezone import now
from datetime import timedelta, datetime



my_logger = logging.getLogger("datacollector")



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



def with_buttons_address_block(language,address):

    header = replies_text(R.AskBlock.ADDRESS_HEADER, language)
    body = replies_text(R.AskBlock.ADDRESS_BODY, language)
    body += f"\n{address}"
    footer = replies_text(R.AskBlock.ADDRESS_FOOTER, language)

    confirm_button = replies_text(R.AskBlock.Buttons.CONFIRM, language)
    change_button = replies_text(R.AskBlock.Buttons.CHANGE, language)


    buttons = [
        {
            "title": confirm_button,
            "value": "datacollector|address_confirmed"
        },
        {
            "title": change_button,
            "value": "datacollector|ask_address"
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





def get_delivery_slots():
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
            "title": "Доступные слоты",
            "rows": [],
        }
    ]
    start_time = now()
    rows = []

    if start_time.hour < 13:
        rows.append(
            {
                "title": "Сегодня с 15:00 до 20:00",
                "value": "today_15_20",
                "description": f"{start_time.day} с 15:00 до 20:00"}
        )
        tommorow = start_time + timedelta(days=1)

    rows.append(
        {
            "title": "Завтра с 9:00 до 15:00",
            "value": "tomorrow_9_15",
            "description": f"{tommorow.day} с 9:00 до 15:00"
        }
    )
    rows.append(
        {
            "title": "Завтра с 15:00 до 20:00",
            "value": "tomorrow_15_20",
            "description": f"{tommorow.day} с 15:00 до 20:00"
        }
    )
    tommorow_after = tommorow + timedelta(days=1)

    rows.append(
        {
            "title": "Послезавтра с 9:00 до 15:00",
            "value": "aftertomorrow_9_15",
            "description": f"{tommorow_after} с 9:00 до 15:00"
        }
    )

    rows.append(
        {
            "title": "Послезавтра с 15:00 до 20:00",
            "value": "aftertomorrow_15_20",
            "description": f"{tommorow_after} с 15:00 до 20:00"
        }
    )





def collect_data_before_order(the_way,
                              language,
                              user_phone,
                              what_next_comment=None,
                              what_next_details=None,
                              ) -> dict:
    """
    the_way = catch_address (action=datacollecter|catch_address)
    what_next_comment = сообщение об ошибке
    what_next_details = содержимое
    """

    result = None
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

        case "change_address":
            """Надо поменять адрес"""
            header = replies_text(R.AskBlock.ADDRESS_HEADER, language)
            client.address = None
            client.save()
            result = no_buttons_address_block(language)

        case "catch_address":
            my_logger.info("Поймал Адрес")
            new_address = what_next_details
            client.address = new_address
            client.save()
            menu = {}

            menu_block = {
                "header": replies_text(R.AskBlock.SPOT_HEADER, language),
                "body": replies_text(R.AskBlock.SPOT_BODY, language),
                "footer": replies_text(R.AskBlock.SPOT_FOOTER, language),
                "list_title": replies_text(R.AskBlock.SPOT_TITLE, language),
                "section_title": replies_text(R.AskBlock.SPOT_SECTION, language)
            }

            buttons = get_delivery_slots()

            menu['what_next'] = 'create_menu'
            menu['menu_block'] = menu_block
            menu['menu_buttons'] = buttons
            result = menu
            #FIXME

        case "address_confirmed":
            """у нас подтвержденный адрес тогда переходим к опросу про доставку"""

            header = replies_text(R.AskBlock.ADDRESS_HEADER, language)
            body = replies_text(R.AskBlock.ADDRESS_BODY, language)
            footer = replies_text(R.AskBlock.ADDRESS_FOOTER, language)

            infoblock = {
                "header": header,
                "body": body,
                "footer": footer
            }

            result = {
                'infoblock': {'infoblock_block': infoblock},
                'support_logic': SupportLogic.NO_BUTTONS,
                'next_action': 'datacollector|catch_address'}

        case "delivery_time_ask":
            menu = {}

            menu_block = {
                "header": replies_text(R.AskBlock.SPOT_HEADER, language),
                "body": replies_text(R.AskBlock.SPOT_BODY, language),
                "footer": replies_text(R.AskBlock.SPOT_FOOTER, language),
                "list_title": replies_text(R.AskBlock.SPOT_TITLE, language),
                "section_title": replies_text(R.AskBlock.SPOT_SECTION, language)
            }

            buttons = get_delivery_slots()

            menu['what_next'] = 'create_menu'
            menu['menu_block'] = menu_block
            menu['menu_buttons'] = buttons
            result = menu
    return result











