# Generated by Django 3.2 on 2023-01-03 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='place_code',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='recparam',
            name='place_code',
            field=models.IntegerField(),
        ),
    ]