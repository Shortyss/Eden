# Generated by Django 4.2.7 on 2024-01-09 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0022_remove_hotel_booked_rooms_remove_hotel_total_rooms_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prices',
            name='price_adult',
        ),
        migrations.RemoveField(
            model_name='prices',
            name='price_child',
        ),
        migrations.RemoveField(
            model_name='travelpackage',
            name='price_modifier',
        ),
        migrations.RemoveField(
            model_name='travelpackage',
            name='price_per_day_adult',
        ),
        migrations.RemoveField(
            model_name='travelpackage',
            name='price_per_day_children',
        ),
        migrations.AddField(
            model_name='prices',
            name='price_double_room',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Cena za dvoulůžkový pokoj'),
        ),
        migrations.AddField(
            model_name='prices',
            name='price_family_room',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Cena za rodinný pokoj'),
        ),
        migrations.AddField(
            model_name='prices',
            name='price_single_room',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Cena za jednolůžkový pokoj'),
        ),
        migrations.AddField(
            model_name='prices',
            name='price_suite',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Cena za apartmán'),
        ),
        migrations.AddField(
            model_name='travelpackage',
            name='number_of_rooms',
            field=models.IntegerField(default=0, verbose_name='Celkový počet pokojů'),
        ),
        migrations.AddField(
            model_name='travelpackage',
            name='room_type',
            field=models.CharField(blank=True, choices=[('single', 'Jednolůžkový'), ('double', 'Dvoulůžkový'), ('family', 'Rodinný'), ('suite', 'Apartmán')], max_length=16, null=True, verbose_name='Typ pokoje'),
        ),
    ]