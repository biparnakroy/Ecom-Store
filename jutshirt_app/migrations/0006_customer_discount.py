# Generated by Django 4.0.4 on 2022-04-24 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jutshirt_app', '0005_customer_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='discount',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]