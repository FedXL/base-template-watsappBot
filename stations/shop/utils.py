from api_backend.models import Variables


def cart_buttons_generator(items,cart_summary,language):
    required_variables = ('cart', 'submit_order', 'submit_order_description',
                          'clear_cart', 'clear_cart_description', 'comeback', 'comeback_description')
    items_count = len(items)
    variables = {var.name: var for var in Variables.objects.filter(name__in=required_variables)}

    cart_name = getattr(variables['cart'], language)
    submit_order = getattr(variables['submit_order'], language)
    submit_order_description = getattr(variables['submit_order_description'], language)

    clean_cart = getattr(variables['clear_cart'], language)
    clean_cart_description = getattr(variables['clear_cart_description'], language)

    comeback = getattr(variables['comeback'], language)
    comeback_description = getattr(variables['comeback_description'], language)



    base_buttons = {
        'title': cart_name,
        'rows': []
    }


    submit_order_description = f"{submit_order_description} {cart_summary} ₸."

    comeback_button = {'title': comeback, 'value': 'create_menu_main', 'description': comeback_description}
    submit_order_button = {'title': submit_order, 'value': 'create_order', 'description': submit_order_description}
    clear_cart_button = {'title': clean_cart, 'value': 'clear_cart', 'description': clean_cart_description}



    if items_count == 0:
        base_buttons['rows'].append(comeback_button)
    elif items_count <=7:

        for item in items:
            item_dict = item.to_dict()
            name_of_product = item_dict.get("product_header_rus") if language == 'rus' else item.product.header_rus
            button_title = f"{name_of_product}"
            total_price = item.total_price
            button_description = f"{item.product.price} Х {item.quantity} = {total_price} ₸."
            base_buttons['rows'].append({
                'title': button_title[:23],
                'value': f"create_productblock_{item.product.product_name}",
                'description': f" {button_description[:64]}"
            })

        base_buttons['rows'].append(submit_order_button)
        base_buttons['rows'].append(clear_cart_button)
        base_buttons['rows'].append(comeback_button)

    return base_buttons
