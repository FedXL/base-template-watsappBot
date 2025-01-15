import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from api_backend.models import MenuBlock, InfoBlock, Variables
from clients.models import Client


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

        client, created = Client.objects.update_or_create(
            phone=phone,
            defaults={
                'username': username,
                'session': session_v,
            }
        )
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

def infoblock_serializer(infoblock_name, language, for_operator_link = False)-> tuple:
    infoblock_obj = InfoBlock.objects.filter(name=infoblock_name).first()

    if not infoblock_obj:
        False, False

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
    return infoblock_block , buttons

class SummonBlockApiView(APIView):
    permission_classes = [IsAuthenticated]
    logger = logging.getLogger('Views| Summon')

    def post(self, request):
        result_data = {}
        action = request.data.get('what_next')
        language = request.data.get('language')

        if "create_menu" in action:
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
            self.logger.info(f'Creating infoblock {action}')
            infoblock_result = {}
            result_data['what_next'] = action
            name_infoblock = action.replace('create_infoblock_', '')
            infoblock_block,buttons=infoblock_serializer(name_infoblock,language)
            infoblock_result['infoblock_block'] = infoblock_block
            infoblock_result['buttons'] = buttons
            result_data['infoblock'] = infoblock_result
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


            


