from api_backend.models import Variables

def replies_text(name, language) -> str:
    assert language in ["rus", "kaz", "RU", "KAZ", "RUS"], "Language must be 'rus' or 'kaz'"
    if language in ["RU", "KAZ", "RUS","RU","rus"]:
        language = 'rus'
    else:
        language = 'kaz'
    variable = Variables.objects.filter(name=name).first()
    text = getattr(variable, language)
    return text

WATER_19L_BOTTLE = 'water_19L'


class R:
    class Navigate:
        COMEBACK = "comeback"
        YES = "yes"
        NO = "no"

    class Variables:
        QUANTITY = "quantity"
        COLLECT_DATA_ASK = "collect_data_ask"
        COLLECT_DATA_TEXT = "collect_data_text"

    class AskBlock:
        DELIVERY = "delivery_type_ask"

        ADDRESS_HEADER = "address_ask_header"
        ADDRESS_BODY = "address_ask_body"
        ADDRESS_FOOTER = "address_ask_footer"

        CONTAINER_HEADER = "container_ask_header"
        CONTAINER_BODY = "container_ask_body"
        CONTAINER_FOOTER = "container_ask_footer"

        SPOT_HEADER = "spot_ask_header"
        SPOT_BODY = "spot_ask_body"
        SPOT_FOOTER = "spot_ask_footer"
        SPOT_TITLE = "spot_ask_title"
        SPOT_SECTION = "spot_ask_section"

        TODAY_15_20 = "today_15_20"
        TOMORROW_9_15 = "tomorrow_9_15"
        TOMORROW_15_20 = "tomorrow_15_20"
        AFTER_TOMORROW_9_15 = "after_tomorrow_9_15"
        AFTER_TOMORROW_15_20 = "after_tomorrow_15_20"

        class Buttons:
            CONFIRM = "address_ask_confirm"
            CHANGE = "address_ask_change"

        PAYMENT =  "payment_ask"





class SupportLogic:
    NO_BUTTONS =  'no_buttons'
    WITH_BUTTONS = 'with_buttons'