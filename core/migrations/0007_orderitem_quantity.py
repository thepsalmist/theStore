# Generated by Django 2.2.7 on 2019-11-13 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_item_discount_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
