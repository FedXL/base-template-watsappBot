from django.db import models



class Client(models.Model):
    phone = models.CharField(max_length=30, verbose_name="Телефон", unique=True)
    username = models.CharField(max_length=150, verbose_name="WatsApp Username")
    last_visit = models.DateTimeField(auto_now=True, verbose_name="Последний визит")
    first_visit = models.DateTimeField(auto_now_add=True, verbose_name="Первый визит")
    comment = models.TextField(null=True, blank=True, verbose_name='Комментарии о посетителе',
                               default='Нет комментариев')


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