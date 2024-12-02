from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
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

    def post(self, request):
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        session = request.POST.get('session')
        client,create = Client.objects.create_or_update(phone=phone,username=username,session=session)
        return Response({'message': 'ok!'})