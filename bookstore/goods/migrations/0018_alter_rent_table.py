# Generated by Django 4.0.6 on 2022-08-24 09:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0017_delete_purchase'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='rent',
            table='goods_rent',
        ),
    ]
