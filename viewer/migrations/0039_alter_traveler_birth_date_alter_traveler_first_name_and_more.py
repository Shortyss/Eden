# Generated by Django 4.2.7 on 2024-01-24 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0038_traveler_purchase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traveler',
            name='birth_date',
            field=models.DateField(blank=True, default=None, null=True, verbose_name='Datum narození'),
        ),
        migrations.AlterField(
            model_name='traveler',
            name='first_name',
            field=models.CharField(blank=True, max_length=68, null=True, verbose_name='Jméno'),
        ),
        migrations.AlterField(
            model_name='traveler',
            name='last_name',
            field=models.CharField(blank=True, max_length=68, null=True, verbose_name='Příjmení'),
        ),
    ]
