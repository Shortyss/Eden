# Generated by Django 4.2.7 on 2023-12-24 09:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0007_alter_city_country_alter_country_continent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='Country',
            new_name='country',
        ),
        migrations.RenameField(
            model_name='country',
            old_name='Continent',
            new_name='continent',
        ),
    ]
