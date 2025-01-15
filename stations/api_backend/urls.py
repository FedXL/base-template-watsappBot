from django.urls import path
from api_backend.views import HelloApiView, CollectClientData, SummonBlockApiView

urlpatterns = [
    path('hello/', HelloApiView.as_view(), name='hello'),
    path('clients/collect/', CollectClientData.as_view(), name='collect'),
    path('summon/', SummonBlockApiView.as_view(), name='summon'),
]