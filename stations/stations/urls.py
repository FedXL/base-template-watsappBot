from django.contrib import admin
from django.urls import path, include
from api_backend.views import IsDead

admin.site.site_header = "Nomad Water BOT"
admin.site.site_title = "Nomad Water Admin Portal"
admin.site.index_title = "Добро пожаловать в Nomad Water"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api_backend.urls')),
    path('', IsDead.as_view(), name='is_dead'),
]
