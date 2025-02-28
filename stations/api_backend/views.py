import logging
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api_backend.handlers.ask_way import collect_data_before_order
from api_backend.handlers.collect_data.collect_cart_quantity import collect_product_quantity_way
from api_backend.handlers.create_order import create_order, create_text_success
from api_backend.models import MenuBlock, InfoBlock, Variables, ProductBlock
from api_backend.replies import R, replies_text
from api_backend.utils import infoblock_serializer, client_cart_serializer, create_product_block_data
from clients.models import Client
from shop.models import Cart

class HelloApiView(APIView):
    def get(self, request):
        return Response({'message': 'Hello World!'})

class SummonMenu(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        token = request.data.get('token')
        return Response({'message': 'Summon Menu!'})

class CollectClientData(APIView):
    permission_classes = [IsAuthenticated]
    logger = logging.getLogger('Views| collect client data')
    def post(self, request):
        message = None
        self.logger.info(f'Collecting client data... {request.data}')
        phone = request.data.get('phone')
        session_v = request.data.get('session')
        username = request.data.get('username')
        if not username and not phone:
            username = 'Tester'
            phone = '1234567890'
        if username == 'None' and phone == 'None':
            username = 'Tester'
            phone = '1234567890'
        try:
            with transaction.atomic():
                client, created = Client.objects.update_or_create(
                    phone=phone,
                    defaults={
                        'username': username,
                        'session': session_v,
                    }
                )
                if created:
                    Cart.objects.create(client=client)
        except Exception as e:
            message = f'Error: {e}'
        if not message:
            message = 'Client created!' if created else 'Client updated!'
        return Response({'message': message})


def menu_serializer(menu, language,my_logger):
    my_logger.info(f'Menu serializer {menu} {language}')
    menu_buttons = {}
    menu_obj = MenuBlock.objects.filter(name=menu).first()
    if not menu_obj:
        return False, False
    menu_block = menu_obj.block_to_dict(language)
    menu_buttons['title'] = menu_block['section_title']
    buttons = menu_obj.buttons.all().order_by('button_number')
    rows = []
    for button in buttons:
        row = button.to_dict(language)
        rows.append(row)
    if menu == 'main':
        if language == 'rus':
            rows.append({
                "title": "Корзина",
                "value": "create_special_menu_cart",
                "description": "Просмотреть содержимое корзины"
            })
            rows.append({
                "title": "Назад",
                "value": "to_language_choice",
                "description": "Назад к выбору языка"
            })
        elif language == 'kaz':
            rows.append({
                "title": "Себет",
                "value": "create_special_menu_cart",
                "description": "Себеттің мазмұнын көру"
            })
            rows.append({
                "title": "Артқа",
                "value": "to_language_choice",
                "description": "Тілді таңдауға қайту"
            })

    menu_buttons['rows'] = rows

    return menu_block, menu_buttons


class SummonBlockApiView(APIView):

    permission_classes = [IsAuthenticated]
    logger = logging.getLogger('Views| Summon')

    def post(self, request):
        result_data = {}
        if request.data == None:
            return Response({'message': 'Data not found!'}, status=404)
        action = request.data.get('what_next',None)
        language = request.data.get('language', None)
        user_phone = request.data.get('user_phone', None)
        self.logger.info(f'SUMMON BLOCK API Action: {request.data}')
        if not language or language == 'None':
            return Response({'message': 'Language not found!'}, status=404)

        if not action or action == 'None':
            return Response({'message': 'Action not found!'}, status=404)

        if not user_phone or user_phone == 'None':
            user_phone = '1234567890'

        if "create_menu" in action:
            """основная фишка что в меню будет список из кнопок"""
            self.logger.info(f'Creating menu {action}')
            menu_result = {}
            result_data['what_next'] = action
            menu = action.replace('create_menu_', '')
            menu_block, menu_buttons = menu_serializer(menu, language, self.logger)
            if not menu_block:
                return Response({'message': 'Menu not found!'})
            menu_result['menu_block'] = menu_block
            menu_result['menu_buttons'] = [menu_buttons]
            result_data['menu'] = menu_result
            return Response(result_data, status=200)


        elif 'create_infoblock' in action:
            """основная фишка что в меню три кнопки будет"""
            self.logger.info(f'Creating infoblock {action}')
            infoblock_result = {}
            result_data['what_next'] = action
            name_infoblock = action.replace('create_infoblock_', '')
            infoblock_block, buttons = infoblock_serializer(name_infoblock, language)
            infoblock_result['infoblock_block'] = infoblock_block
            infoblock_result['buttons'] = buttons
            result_data['infoblock'] = infoblock_result
            return Response(result_data, status=200)


        elif 'create_productblock_' in action:
            """основная фишка что в меню (три) кнопки будет по управлению корзиной"""
            self.logger.info(f'Creating product {action}')
            result_data['what_next'] = action
            product_name = action.replace('create_productblock_', '')
            result_data['product_name'] = product_name
            is_success, comment_or_result = create_product_block_data(action=action,
                                                                      language=language,
                                                                      user_phone=user_phone,
                                                                      result_data=result_data)
            if not is_success:
                return Response({'message': comment_or_result}, status=404)
            return Response(comment_or_result, status=200)

        elif 'remove_from_cart_' in action:
            self.logger.info(f'Removing from cart {action}')
            product_name = action.replace('remove_from_cart_', '')
            result_data['product_name'] = product_name
            result_data['what_next'] = 'create_productblock_' + product_name
            client = Client.objects.filter(phone=user_phone).first()
            cart = client.cart_related
            cart_item = cart.cart_items.filter(product__product_name=product_name).first()
            if not cart_item:
                return Response({'message': 'Product not found in cart!'}, status=404)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
            is_success, comment_or_result = create_product_block_data(action=action, language=language,
                                                                      user_phone=user_phone, result_data=result_data)
            if not is_success:
                return Response({'message': comment_or_result}, status=404)
            return Response(comment_or_result, status=200)

        elif action =='create_order':
            """создаем заказ"""

            is_created = create_order(user_phone, self.logger)
            self.logger.info(f'Creating order {is_created}')
            result_data = create_text_success(language, is_created)
            return Response(result_data, status=200)

        elif 'create_special_menu_' in action:
            """всякие хитрые блоки со списками"""
            self.logger.info(f'Creating special menu {action}')
            what_kind_of_special = action.replace('create_special_menu_', '')
            self.logger.info(f'Creating special menu {what_kind_of_special}')

            match what_kind_of_special:
                case 'cart':
                    result_data['what_next'] = 'create_menu_cart'
                    client = Client.objects.filter(phone=user_phone).first()
                    cart_buttons = client.cart_related.shopping_cart_buttons(language)
                    summary_price = client.cart_related.total_price
                    cart_name = Variables.objects.filter(
                        name='cart').first().rus if language == 'rus' else Variables.objects.filter(
                        name='cart').first().kaz
                    if summary_price == 0:
                        cart_body = replies_text(R.Cart.EMPTY_CART, language=language)
                    else:
                        cart_body = replies_text(name=R.Cart.BODY, language=language)
                        cart_body += f' {summary_price} ₸.'
                    result_data['menu'] = {
                        "menu_block": {
                            "header": replies_text(name=R.Cart.HEADER, language=language),
                            "body": cart_body,
                            "footer": replies_text(name=R.Cart.FOOTER, language=language),
                            "list_title": replies_text(name=R.Cart.LIST_TITLE, language=language),
                            "section_title": replies_text(name=R.Cart.SECTION_TITLE, language=language)
                        },
                        "menu_buttons": [cart_buttons]
                    }
                    return Response(result_data, status=200)

        elif action == 'to_language_choice':
            self.logger.info(f'Going to language choice')
            result_data['what_next'] = action
            return Response(result_data, status=200)

        elif 'datacollector' in action:
            self.logger.info(f'DATACOLLECTOR START')
            parsing_variable = None
            comment = request.data.get('what_next_comment', None)
            collected_data = request.data.get('what_next_details', None)
            the_way = action.split('|')[1]
            self.logger.info(f"the_way: {the_way}")
            try:
                parsing_variable = action.split('|')[2]
                self.logger.info(f"parsing_variable: {parsing_variable}")
            except:
                self.logger.error(f"parsing_variable not found")
                pass
            try:
                assert the_way in ['ask_address','catch_address','catch_time',
                            'ask_about_container','ask_about_delivery',
                            'ask_about_payment','product_quantity','catch_product_quantity'], 'The way not found'
            except:
                return Response({'message': 'The way not found!'}, status=404)
            self.logger.info(f'Collecting data before order {the_way}')
            result = collect_data_before_order(
                                the_way=the_way,
                                what_next_comment=comment,
                                what_next_details=collected_data,
                                language=language,
                                user_phone=user_phone,
                                parsing_variable=parsing_variable,
                                my_logger=self.logger
                )
            return Response(result, status=200)

        elif "create_operator_link_from_" in action:
            self.logger.info(f'Creating operator link from {action}')
            result_data['what_next'] = action
            infoblock_name = action.replace('create_operator_link_from_', '')
            self.logger.info(f'Creating operator link from {infoblock_name}')
            infoblock = InfoBlock.objects.filter(name=infoblock_name).first()
            self.logger.info(f'Infoblock: {infoblock}')
            operator_phone = Variables.objects.filter(name='operator_phone').first().rus

            if language == 'rus':
                info = infoblock.header_rus
                prefix = 'Здравствуйте, меня интересует информация по '
                operator_header = Variables.objects.filter(name='operator_header').first().rus
                operator_footer = Variables.objects.filter(name='operator_footer').first().rus
            elif language == 'kaz':
                prefix = 'Сәлеметсіз бе, маған ақпарат керек'
                info = infoblock.header_kaz
                operator_header = Variables.objects.filter(name='operator_header').first().kaz
                operator_footer = Variables.objects.filter(name='operator_footer').first().kaz
            if info:
                text = prefix + info
                text = text.replace(' ', '%20')
                link = f"https://wa.me/{operator_phone}?text={text}"

            else:
                link = f"https://wa.me/{operator_phone}"

            self.logger.warning(f"infoblock name {infoblock_name}")
            infoblock_block, buttons = infoblock_serializer(infoblock_name,
                                                            language,
                                                            for_operator_link=True)

            result_data['infoblock'] = {
                'link': link,
                'buttons': buttons,
                'infoblock_block': {
                    'header': operator_header,
                    'footer': operator_footer
                }
            }
            return Response(result_data, status=200)

        else:
            body = f'Action {action} not found!'
            return Response({'message': 'Action not found!',
                             'action was':action,
                             'what_next': body},
                            status=404)

class IsDead(APIView):
    def get(self, request):
        return Response({'message': 'I am not dead!'})
#
# class CollectCartQuantity(APIView):
#     permission_classes = [IsAuthenticated]
#     logger = logging.getLogger('Views| Collect Data Text')
#
#     def post(self, request):
#         result_data = {}
#
#         if request.data == None:
#             return Response(data={'message': 'Data not found!'}, status=404)
#
#         action = request.data.get('what_next',None)
#         language = request.data.get('language',None)
#         user_phone = request.data.get('user_phone', None)
#         text_data = request.data.get('text_data', None)
#
#         self.logger.info(f'Collecting data text... {request.data}')
#         if not language or language == 'None':
#             return Response({'message': 'Language not found!'}, status=404)
#
#         if not action or action == 'None':
#             return Response({'message': 'Action not found!'}, status=404)
#
#         if not user_phone or user_phone == 'None':
#             user_phone = '1234567890'
#
#         if not text_data or text_data == 'None':
#             text_data = 'No data'
#         if 'text' in action and 'cart_quantity' in action:
#             product, what_next, comment = collect_product_quantity_way(action=action, language=language,
#                                                                     user_phone=user_phone, text_data=text_data)
#             self.logger.info(f'Collecting product quantity {product} | {what_next} | {comment}')
#             datta = {"what_next": what_next,
#                      'product_name':product}
#             result_data['product_name'] = product
#             result_data['what_next_from_way']= what_next
#
#             if what_next:
#                 is_success, comment_or_result = create_product_block_data(action=action,
#                                                                       language=language,
#                                                                       user_phone=user_phone,
#                                                                       result_data=datta)
#                 if is_success:
#                     result_data = {**result_data, **comment_or_result, 'action': action}
#                     return Response(result_data, status=200)
#                 else:
#                     what_next = ("collect_data_text_" + action.replace('collect_data_text_', '').split('|')[0]
#                              + f"|cart_quantity|{comment}")
#                     self.logger.error(f'Error in collect_data_text in create_productblock: {comment}')
#                     self.logger.error(f'Error in collect_data_text: {what_next}')
#                     return Response({'error': comment,
#                      'what_next': what_next}, status=404)
#             else:
#                 what_next = ("collect_data_text_" + action.replace('collect_data_text_', '').split('|')[0]
#                              + f"|cart_quantity|{comment}")
#                 self.logger.error(f'Error in незнаю где но : {comment}')
#                 self.logger.error(f'Error in незнаю где но : {what_next}')
#                 return Response(data={'error': comment,
#                      'what_next': what_next},
#                                 status=404)
