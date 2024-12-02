# admin.py

from django.contrib import admin
from .models import MenuBlock, InfoBlock, ButtonMenu

@admin.register(MenuBlock)
class MenuBlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(InfoBlock)
class InfoBlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)

@admin.register(ButtonMenu)
class ButtonMenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'menu', 'title_rus', 'title_kaz', 'info_block', 'menu_block', 'button_number')
    list_display_links = ('id', 'menu')
    search_fields = ('menu__name', 'title_rus', 'title_kaz', 'info_block__name', 'menu_block__name', 'button_number')
    list_filter = ('menu', 'info_block', 'menu_block')