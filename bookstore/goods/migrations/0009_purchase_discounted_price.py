# Generated by Django 4.0.6 on 2022-08-15 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0008_remove_purchase_discounted_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='discounted_price',
            field=models.IntegerField(default=0, verbose_name='Price with discount'),
        ),
    ]
