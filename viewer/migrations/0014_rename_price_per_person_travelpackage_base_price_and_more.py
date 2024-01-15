# Generated by Django 4.2.7 on 2023-12-29 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0013_alter_airport_airport_city_alter_airport_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='travelpackage',
            old_name='price_per_person',
            new_name='base_price',
        ),
        migrations.RemoveField(
            model_name='travelpackage',
            name='price_per_child',
        ),
        migrations.AddField(
            model_name='travelpackage',
            name='arrival_airport',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='arrival_airport', to='viewer.airport', verbose_name='Letiště přílet'),
        ),
        migrations.AddField(
            model_name='travelpackage',
            name='departure_airport',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, related_name='departure_airport', to='viewer.airport', verbose_name='Letiště odlet'),
        ),
        migrations.AddField(
            model_name='travelpackage',
            name='price_modifier',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Upravená cena'),
        ),
    ]
