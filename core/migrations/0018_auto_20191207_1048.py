# Generated by Django 3.0 on 2019-12-07 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20191206_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='Items/%Y/%M/%d'),
        ),
    ]
