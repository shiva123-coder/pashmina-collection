# Generated by Django 3.2.23 on 2024-03-14 16:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0004_alter_coupon_discount_amount'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Coupon',
        ),
    ]
