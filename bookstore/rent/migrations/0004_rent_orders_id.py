# Generated by Django 4.0.6 on 2022-08-25 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rent', '0003_rent_address_rent_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='rent',
            name='orders_id',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='ID of order'),
        ),
    ]
