# Generated by Django 4.2.7 on 2024-01-29 17:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0047_roomavailability_room_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roomavailability',
            old_name='date',
            new_name='arrival_date',
        ),
        migrations.AddField(
            model_name='roomavailability',
            name='departure_date',
            field=models.DateField(default=datetime.date(2024, 1, 29)),
        ),
    ]