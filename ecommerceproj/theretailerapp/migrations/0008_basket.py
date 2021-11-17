# Generated by Django 3.2.8 on 2021-11-17 08:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('theretailerapp', '0007_customer_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basket_billing_address', models.CharField(help_text='Billing Address', max_length=200)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='theretailerapp.customer')),
                ('products', models.ManyToManyField(to='theretailerapp.Product')),
            ],
        ),
    ]