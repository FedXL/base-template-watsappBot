from django.core.exceptions import ValidationError
from django.db import models


class Block(models.Model):
    header_rus = models.CharField(max_length=59, verbose_name="Заголовок на русском", null=True, blank=True)
    header_kaz = models.CharField(max_length=59, verbose_name="Заголовок на казахском", null=True, blank=True)

    body_rus = models.TextField(max_length=1020, verbose_name="Основной текст на русском")
    body_kaz = models.TextField(max_length=1020, verbose_name="Основной текст на казахском")

    footer_rus = models.CharField(max_length=59, verbose_name="Подвал на русском",null=True, blank=True)
    footer_kaz = models.CharField(max_length=59, verbose_name="Подвал на казахском",null=True, blank=True)


    class Meta:
        abstract = True



class MenuBlock(Block):
    name = models.CharField(max_length=100, verbose_name="Название (не отображается)",unique=True)

    list_title_rus = models.CharField(max_length=19, verbose_name="Заголовок списка на русском")
    list_title_kaz = models.CharField(max_length=19, verbose_name="Заголовок списка на казахском")

    section_title_rus = models.CharField(max_length=23, verbose_name="Заголовок секции на русском")
    section_title_kaz = models.CharField(max_length=23, verbose_name="Заголовок секции на казахском")


    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"

    def __str__(self):
        return self.name

    def block_to_dict(self, language):
        return {
            'header': self.header_rus if language == 'rus' else self.header_kaz,
            'body': self.body_rus if language == 'rus' else self.body_kaz,
            'footer': self.footer_rus if language == 'rus' else self.footer_kaz,
            'list_title': self.list_title_rus if language == 'rus' else self.list_title_kaz,
            'section_title': self.section_title_rus if language == 'rus' else self.section_title_kaz
        }


class InfoBlock(Block):
    name = models.CharField(max_length=100, verbose_name="Название инфоблока для поиска",unique=True)

    body_rus = models.TextField(max_length=2040, verbose_name="Основной текст на русском")
    body_kaz = models.TextField(max_length=2040, verbose_name="Основной текст на казахском")

    class Meta:
        verbose_name = "Инфоблок"
        verbose_name_plural = "Инфоблоки"

    def __str__(self):
        return f"{self.name} - {self.header_rus}"

    def block_to_dict(self, language):
        body_text = self.body_rus if language == 'rus' else self.body_kaz
        if len(body_text) > 1020:
            body_01 = body_text[:1017] + '...'
            body = body_text[:1017]
            return {
                'header': self.header_rus if language == 'rus' else self.header_kaz,
                'body_01': body_01,
                'body':body,
                'footer': self.footer_rus if language == 'rus' else self.footer_kaz
            }
        else:
            return {
                'header': self.header_rus if language == 'rus' else self.header_kaz,
                'body': body_text,
                'footer': self.footer_rus if language == 'rus' else self.footer_kaz
            }



class ButtonMenu(models.Model):
    """Это кнопки в списках меню"""
    menu = models.ForeignKey(MenuBlock, on_delete=models.CASCADE, related_name='buttons', verbose_name="Кнопка будет в этом меню")

    title_rus = models.CharField(max_length=23, verbose_name="Текст в кнопке на русском",null=True, blank=True)
    title_kaz = models.CharField(max_length=23, verbose_name="Текст в кнопке на казахском",null=True, blank=True)

    description_rus = models.CharField(max_length=70, verbose_name="Описание на русском",null=True, blank=True)
    description_kaz = models.CharField(max_length=70, verbose_name="Описание на казахском",null=True, blank=True)

    info_block = models.OneToOneField(InfoBlock, on_delete=models.CASCADE, related_name='info_button_reverse', verbose_name="При нажатии переход в этот инфоблок",null=True, blank=True)
    menu_block = models.ForeignKey(MenuBlock, on_delete=models.CASCADE, related_name='menu_button_reverse', verbose_name="При нажатии переход в это меню",null=True, blank=True)


    button_number = models.IntegerField(verbose_name="Порядковый номер", default=0)

    def clean(self):
        super().clean()
        if self.info_block and self.menu_block:
            raise ValidationError("Only one of 'info_block' or 'menu_block' can be filled.")
        if not self.info_block and not self.menu_block:
            raise ValidationError("One of 'info_block' or 'menu_block' must be filled.")

    class Meta:
        verbose_name = "Кнопка"
        verbose_name_plural = "Кнопки"

    def __str__(self):
        return self.title_rus

    def extract_action(self):
        if self.info_block:
            return f"create_infoblock_{self.info_block.name}"
        return f"create_menu_{self.menu_block.name}"

    def to_dict(self, language):

        return {
            'title': self.title_rus if language == 'rus' else self.title_kaz,
            'description': self.description_rus if language == 'rus' else self.description_kaz,
            'value': self.extract_action()
        }

class Variables(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название реплики (ENG)", unique=True)
    rus = models.TextField(verbose_name="Русская реплика")
    kaz = models.TextField(verbose_name="Казахская реплика")

    reply_type = models.CharField(
        max_length=100,
        verbose_name="Тип реплики",
        default='button',
        choices=[
            ('header', 'Заголовок'),
            ('body', 'Основной текст'),
            ('footer', 'Подвал'),
            ('list_title', 'Заголовок списка'),
            ('section_title', 'Заголовок секции'),
            ('button', 'Кнопка')
        ]
    )

    class Meta:
        verbose_name = "Остальные реплики"
        verbose_name_plural = "Остальные реплики"

    def clean(self):
        super().clean()
        if self.reply_type == 'header':
            if len(self.rus) > 59 or len(self.kaz) > 59:
                raise ValidationError("Length of header should be less than 60 symbols")
        if self.reply_type == 'body':
            if len(self.rus) > 1020 or len(self.kaz) > 1020:
                raise ValidationError("Length of body should be less than 1021 symbols")
        if self.reply_type == 'footer':
            if len(self.rus) > 59 or len(self.kaz) > 59:
                raise ValidationError("Length of footer should be less than 60 symbols")
        if self.reply_type == 'list_title':
            if len(self.rus) > 19 or len(self.kaz) > 19:
                raise ValidationError("Length of list title should be less than 20 symbols")
        if self.reply_type == 'section_title':
            if len(self.rus) > 23 or len(self.kaz) > 23:
                raise ValidationError("Length of section title should be less than 24 symbols")
        if self.reply_type == 'button':
            if len(self.rus) > 19 or len(self.kaz) > 19:
                raise ValidationError("Length of button title should be less than 20 symbols")