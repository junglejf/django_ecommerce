# Generated by Django 2.2.4 on 2019-12-19 04:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carrinho', '0003_cart_selected'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='selected',
        ),
    ]
