# Generated by Django 4.2.7 on 2024-01-29 17:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0048_rename_date_roomavailability_arrival_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomavailability',
            name='departure_date',
            field=models.DateField(default=datetime.date(2024, 2, 5)),
        ),
    ]
