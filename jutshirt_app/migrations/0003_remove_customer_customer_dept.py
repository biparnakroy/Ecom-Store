# Generated by Django 4.0.4 on 2022-04-23 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jutshirt_app', '0002_remove_customer_customer_faculty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='customer_dept',
        ),
    ]