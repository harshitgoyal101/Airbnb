# Generated by Django 3.2.5 on 2023-03-19 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0006_hotel_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotel',
            name='index',
            field=models.CharField(max_length=3),
        ),
    ]
