# Generated by Django 3.0.5 on 2020-06-02 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_auto_20200601_0013'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_deal',
            field=models.BooleanField(default=False),
        ),
    ]