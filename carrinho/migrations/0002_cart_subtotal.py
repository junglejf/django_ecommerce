# Generated by Django 2.2.4 on 2019-12-16 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carrinho', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=100),
        ),
    ]
