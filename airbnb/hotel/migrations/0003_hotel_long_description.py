# Generated by Django 3.2.5 on 2023-03-12 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0002_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='long_description',
            field=models.TextField(null=True),
        ),
    ]
