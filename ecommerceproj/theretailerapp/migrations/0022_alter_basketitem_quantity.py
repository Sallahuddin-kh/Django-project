# Generated by Django 3.2.8 on 2021-12-01 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theretailerapp', '0021_auto_20211201_0732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basketitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]