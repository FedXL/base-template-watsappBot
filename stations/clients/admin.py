from django.contrib import admin

from clients.models import Client, ReportEmail


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone', 'first_visit', 'last_visit')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'phone')
    list_filter = ('username', 'phone')
    list_per_page = 25

@admin.register(ReportEmail)
class ReportEmailAdmin(admin.ModelAdmin):
    list_display = ('id', 'email')
    list_display_links = ('id', 'email')
    search_fields = ('email',)
    list_filter = ('email',)
    list_per_page = 25
