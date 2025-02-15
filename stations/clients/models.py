from django.db import models



class Client(models.Model):
    phone = models.CharField(max_length=30, verbose_name="Телефон", unique=True,null=True)
    username = models.CharField(max_length=150, verbose_name="WatsApp Username")
    session = models.CharField(max_length=150, verbose_name="Сессия", null=True, blank=True)
    last_visit = models.DateTimeField(auto_now=True, verbose_name="Последний визит")
    first_visit = models.DateTimeField(auto_now_add=True, verbose_name="Первый визит")
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарии о посетителе',
                               default='Нет комментариев')

    address = models.CharField(max_length=400, verbose_name="Адрес", null=True, blank=True)


    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Посетитель"
        verbose_name_plural = "Посетители"

class ReportEmail(models.Model):
    email = models.EmailField(verbose_name="Email для рассылки отчетов")

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Email для рассылки"
        verbose_name_plural = "Email для рассылки"