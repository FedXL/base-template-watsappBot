from django.urls import path
from .views import HelloApiView, CollectClientData, SummonBlockApiView, CollectCartQuantity

urlpatterns = [
    path('hello/', HelloApiView.as_view(), name='hello'),
    path('clients/collect/', CollectClientData.as_view(), name='collect'),
    path('summon/', SummonBlockApiView.as_view(), name='summon'),
    path('summon/collect_data/', CollectCartQuantity.as_view(), name='collect_cart_quantity'),
]