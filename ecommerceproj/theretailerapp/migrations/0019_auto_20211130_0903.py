# Generated by Django 3.2.8 on 2021-11-30 09:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('theretailerapp', '0018_order_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='approval_status',
        ),
        migrations.DeleteModel(
            name='ApprovalStatus',
        ),
    ]
