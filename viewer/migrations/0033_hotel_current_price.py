# Generated by Django 4.2.7 on 2024-01-19 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0032_remove_purchase_traveler_purchase_travelers'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='current_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Aktuální cena'),
        ),
    ]
