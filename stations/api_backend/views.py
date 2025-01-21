import logging

from django.conf import settings
from django.db import transaction
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import is_success
from rest_framework.views import APIView
from api_backend.models import MenuBlock, InfoBlock, Variables, ProductBlock
from api_backend.utils import infoblock_serializer, client_card_serializer, create_product_block_data
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
        message=None
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

def menu_serializer(menu, language):
    menu_buttons={}
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
        if language =='rus':
            rows.append({
                "title": "Назад",
                "value": "to_language_choice",
                "description": "Назад к выбору языка"
                })
        else:
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
        action = request.data.get('what_next')
        language = request.data.get('language')
        user_phone = request.data.get('user_phone', None)
        if not user_phone or user_phone == 'None':
            user_phone = '1234567890'
        if "create_menu" in action:
            """основная фишка что в меню будет список из кнопок"""
            self.logger.info(f'Creating menu {action}')
            menu_result = {}
            result_data['what_next'] = action
            menu = action.replace('create_menu_', '')
            menu_block, menu_buttons = menu_serializer(menu,language)
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
            infoblock_block, buttons = infoblock_serializer(name_infoblock,language)
            infoblock_result['infoblock_block'] = infoblock_block
            infoblock_result['buttons'] = buttons
            result_data['infoblock'] = infoblock_result
            return Response(result_data, status=200)

        elif 'create_productblock_' in action:
            """основная фишка что в меню две (три) кнопки будет по управлению корзиной"""
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
        elif 'add_to_cart_' in action:
            self.logger.info(f'Adding to cart {action}')
            product_name = action.replace('add_to_cart_', '')
            result_data['product_name'] = product_name
            result_data['what_next'] = 'create_productblock_' + product_name
            client = Client.objects.filter(phone=user_phone).first()
            cart = client.cart_related
            product = ProductBlock.objects.filter(product_name=product_name).first()
            if not product:
                return Response({'message': 'Product not found!'}, status=404)
            cart_item, created = cart.cart_items.get_or_create(product=product)
            if not created:
                cart_item.quantity += 1
                cart_item.save()
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
            is_success, comment_or_result = create_product_block_data(action=action,
                                                                        language=language,
                                                                        user_phone=user_phone,
                                                                        result_data=result_data)
            if not is_success:
                return Response({'message': comment_or_result}, status=404)
            return Response(comment_or_result, status=200)

        elif 'create_special_menu_' in action:
            self.logger.info(f'Creating special menu {action}')
            what_kind_of_special = action.replace('create_special_menu_', '')
            self.logger.info(f'Creating special menu {what_kind_of_special}')
            result_data['what_next'] = 'create_menu_cart'
            client = Client.objects.filter(phone=user_phone).first()
            cart_buttons = client.cart_related.shopping_card_buttons(language)
            content = client.cart_related.shopping_card_content()
            result_data['menu']= {
                "menu_block": {
                    "header": "Корзина",
                    "body": f'Содержимое корзины {str(content)}',
                    "footer": 'заказать или очистить корзину',
                    "list_title": "Меню",
                    "section_title": "Меню"
                },
                "menu_buttons": [cart_buttons]
            }



            return Response(result_data, status=200)


        elif action == 'to_language_choice':
            self.logger.info(f'Going to language choice')
            result_data['what_next'] = action
            return Response(result_data, status=200)





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
            infoblock_block, buttons=infoblock_serializer(infoblock_name, language, for_operator_link=True)
            result_data['infoblock'] = {
                'link': link,
                'buttons': buttons,
                'infoblock_block': {'header': operator_header, 'footer': operator_footer}
            }
            return Response(result_data, status=200)



        else:
            return Response({'message': 'Action not found!'}, status=404)


            

class IsDead(APIView):
    def get(self, request):
        return Response({'message': 'I am not dead!'})
