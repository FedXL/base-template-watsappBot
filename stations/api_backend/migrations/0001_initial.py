# Generated by Django 5.1.3 on 2025-01-19 17:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header_rus', models.CharField(blank=True, max_length=59, null=True, verbose_name='Заголовок на русском')),
                ('header_kaz', models.CharField(blank=True, max_length=59, null=True, verbose_name='Заголовок на казахском')),
                ('footer_rus', models.CharField(blank=True, max_length=59, null=True, verbose_name='Подвал на русском')),
                ('footer_kaz', models.CharField(blank=True, max_length=59, null=True, verbose_name='Подвал на казахском')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название инфоблока для поиска')),
                ('body_rus', models.TextField(max_length=2040, verbose_name='Основной текст на русском')),
                ('body_kaz', models.TextField(max_length=2040, verbose_name='Основной текст на казахском')),
            ],
            options={
                'verbose_name': 'Инфоблок',
                'verbose_name_plural': 'Инфоблоки',
            },
        ),
        migrations.CreateModel(
            name='MenuBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header_rus', models.CharField(blank=True, max_length=59, null=True, verbose_name='Заголовок на русском')),
                ('header_kaz', models.CharField(blank=True, max_length=59, null=True, verbose_name='Заголовок на казахском')),
                ('body_rus', models.TextField(max_length=1020, verbose_name='Основной текст на русском')),
                ('body_kaz', models.TextField(max_length=1020, verbose_name='Основной текст на казахском')),
                ('footer_rus', models.CharField(blank=True, max_length=59, null=True, verbose_name='Подвал на русском')),
                ('footer_kaz', models.CharField(blank=True, max_length=59, null=True, verbose_name='Подвал на казахском')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название (не отображается)')),
                ('list_title_rus', models.CharField(max_length=19, verbose_name='Заголовок списка на русском')),
                ('list_title_kaz', models.CharField(max_length=19, verbose_name='Заголовок списка на казахском')),
                ('section_title_rus', models.CharField(max_length=23, verbose_name='Заголовок секции на русском')),
                ('section_title_kaz', models.CharField(max_length=23, verbose_name='Заголовок секции на казахском')),
            ],
            options={
                'verbose_name': 'Меню',
                'verbose_name_plural': 'Меню',
            },
        ),
        migrations.CreateModel(
            name='Variables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название реплики (ENG)')),
                ('rus', models.TextField(verbose_name='Русская реплика')),
                ('kaz', models.TextField(verbose_name='Казахская реплика')),
                ('reply_type', models.CharField(choices=[('header', 'Заголовок'), ('body', 'Основной текст'), ('footer', 'Подвал'), ('list_title', 'Заголовок списка'), ('section_title', 'Заголовок секции'), ('button', 'Кнопка')], default='button', max_length=100, verbose_name='Тип реплики')),
            ],
            options={
                'verbose_name': 'Остальные реплики',
                'verbose_name_plural': 'Остальные реплики',
            },
        ),
        migrations.CreateModel(
            name='ButtonMenu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_rus', models.CharField(blank=True, max_length=23, null=True, verbose_name='Текст в кнопке на русском')),
                ('title_kaz', models.CharField(blank=True, max_length=23, null=True, verbose_name='Текст в кнопке на казахском')),
                ('description_rus', models.CharField(blank=True, max_length=70, null=True, verbose_name='Описание на русском')),
                ('description_kaz', models.CharField(blank=True, max_length=70, null=True, verbose_name='Описание на казахском')),
                ('button_number', models.IntegerField(default=0, verbose_name='Порядковый номер')),
                ('product_block', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='product_button_reverse', to='shop.product', verbose_name='При нажатии переход в этот продукт')),
                ('info_block', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='info_button_reverse', to='api_backend.infoblock', verbose_name='При нажатии переход в этот инфоблок')),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buttons', to='api_backend.menublock', verbose_name='Кнопка будет в этом меню')),
                ('menu_block', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menu_button_reverse', to='api_backend.menublock', verbose_name='При нажатии переход в это меню')),
            ],
            options={
                'verbose_name': 'Кнопка',
                'verbose_name_plural': 'Кнопки',
            },
        ),
    ]
