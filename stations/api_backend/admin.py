from django.contrib import admin
from .models import MenuBlock, InfoBlock, ButtonMenu, Variables, ProductBlock


class InlineButton(admin.TabularInline):
    model = ButtonMenu
    extra = 1
    fk_name = 'menu'


@admin.register(MenuBlock)
class MenuBlockAdmin(admin.ModelAdmin):
    inlines = [InlineButton,]
    list_display = ('id', 'name', 'list_title_rus', 'list_title_kaz',
                    'section_title_rus', 'section_title_kaz')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'list_title_rus', 'list_title_kaz',
                     'section_title_rus', 'section_title_kaz')
    list_filter = ('name',)
    fields = ('name',
              'header_rus','header_kaz',
              'body_rus', 'body_kaz',
              'footer_rus', 'footer_kaz',
              'list_title_rus',
              'list_title_kaz',
              'section_title_rus',
              'section_title_kaz')


@admin.register(InfoBlock)
class InfoBlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'header_rus', 'header_kaz')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'header_rus', 'header_kaz')
    list_filter = ('name',)


@admin.register(ProductBlock)
class ProductBlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'header_rus', 'header_kaz')


@admin.register(ButtonMenu)
class ButtonMenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'menu', 'title_rus', 'title_kaz', 'info_block', 'menu_block', 'button_number')
    list_display_links = ('id', 'menu')
    search_fields = ('menu__name', 'title_rus', 'title_kaz', 'info_block__name', 'menu_block__name', 'button_number')
    list_filter = ('menu', 'info_block', 'menu_block')


@admin.register(Variables)
class VariablesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'reply_type', 'rus', 'kaz')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'rus', 'kaz')
    list_filter = ('reply_type',)


