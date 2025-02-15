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



class R:
    class Navigate:
        COMEBACK = "comeback"

    class Variables:
        QUANTITY = "quantity"
        COLLECT_DATA_ASK = "collect_data_ask"
