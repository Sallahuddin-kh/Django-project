# Generated by Django 3.2.8 on 2021-10-29 13:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('theretailerapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(help_text='Enter a Country name', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular book across whole library', primary_key=True, serialize=False)),
                ('first_name', models.CharField(help_text='Enter first name', max_length=20)),
                ('last_name', models.CharField(help_text='Enter last name', max_length=20)),
                ('shipping_address', models.CharField(help_text='Shipping Address', max_length=200)),
                ('billing_address', models.CharField(help_text='Billing Address', max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('created_at', models.DateField(blank=True, null=True)),
                ('updated_at', models.DateField(blank=True, null=True)),
                ('counrty', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='theretailerapp.country')),
            ],
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
    ]
