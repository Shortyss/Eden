# Generated by Django 4.2.7 on 2024-01-18 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0031_remove_purchase_traveler_purchase_traveler'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='traveler',
        ),
        migrations.AddField(
            model_name='purchase',
            name='travelers',
            field=models.IntegerField(default=1, verbose_name='Počet cestujících'),
        ),
    ]
