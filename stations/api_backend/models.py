from django.core.exceptions import ValidationError
from django.db import models


class Block(models.Model):
    header_rus = models.CharField(max_length=100, verbose_name="Заголовок на русском", null=True, blank=True)
    header_kaz = models.CharField(max_length=100, verbose_name="Заголовок на казахском", null=True, blank=True)

    body_rus = models.TextField(max_length=1000, verbose_name="Основной текст на русском",null=True, blank=True)
    body_kaz = models.TextField(max_length=1000, verbose_name="Основной текст на казахском",null=True, blank=True)

    footer_rus = models.CharField(max_length=100, verbose_name="Подвал на русском",null=True, blank=True)
    footer_kaz = models.CharField(max_length=100, verbose_name="Подвал на казахском",null=True, blank=True)

    list_title_rus = models.CharField(max_length=100, verbose_name="Заголовок списка на русском",null=True, blank=True)
    list_title_kaz = models.CharField(max_length=100, verbose_name="Заголовок списка на казахском",null=True, blank=True)

    class Meta:
        abstract = True

class MenuBlock(Block):
    name = models.CharField(max_length=100, verbose_name="Название меню для поиска",unique=True)

class InfoBlock(Block):
    name = models.CharField(max_length=100, verbose_name="Название инфоблока для поиска",unique=True)


class ButtonMenu(models.Model):
    menu = models.ForeignKey(MenuBlock, on_delete=models.CASCADE, related_name='buttons', verbose_name="Кнопка будет в этом меню")

    title_rus = models.CharField(max_length=100, verbose_name="Текст в кнопке на русском",null=True, blank=True)
    title_kaz = models.CharField(max_length=100, verbose_name="Текст в кнопке на казахском",null=True, blank=True)

    info_block = models.ForeignKey(InfoBlock, on_delete=models.CASCADE, related_name='info_button_reverse', verbose_name="При нажатии переход в этот инфоблок",null=True, blank=True)
    menu_block = models.ForeignKey(MenuBlock, on_delete=models.CASCADE, related_name='menu_button_reverse', verbose_name="При нажатии переход в это меню",null=True, blank=True)

    button_number = models.IntegerField(verbose_name="Порядковый номер", default=0)

    def clean(self):
        super().clean()
        if self.info_block and self.menu_block:
            raise ValidationError("Only one of 'info_block' or 'menu_block' can be filled.")
        if not self.info_block and not self.menu_block:
            raise ValidationError("One of 'info_block' or 'menu_block' must be filled.")

