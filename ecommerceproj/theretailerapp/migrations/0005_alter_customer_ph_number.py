# Generated by Django 3.2.8 on 2021-11-01 07:07

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('theretailerapp', '0004_customer_ph_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='ph_number',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]