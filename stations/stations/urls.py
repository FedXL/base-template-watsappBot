from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Техосмотр рядом"
admin.site.site_title = "Техосмотр рядом Admin Portal"
admin.site.index_title = "Добро пожаловать в Техосмотр рядом"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api_backend.urls')),
]
