# Generated by Django 2.2.4 on 2019-12-19 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrinho', '0002_cart_subtotal'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='selected',
            field=models.IntegerField(default=1),
        ),
    ]
