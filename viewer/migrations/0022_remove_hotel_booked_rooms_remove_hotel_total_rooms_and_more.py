# Generated by Django 4.2.7 on 2024-01-09 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0021_island_city_island'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hotel',
            name='booked_rooms',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='total_rooms',
        ),
        migrations.AddField(
            model_name='travelpackage',
            name='number_of_double_rooms',
            field=models.IntegerField(default=0, verbose_name='Počet dvoulůžkových pokojů'),
        ),
        migrations.AddField(
            model_name='travelpackage',
            name='number_of_family_rooms',
            field=models.IntegerField(default=0, verbose_name='Počet rodinných pokojů'),
        ),
        migrations.AddField(
            model_name='travelpackage',
            name='number_of_single_rooms',
            field=models.IntegerField(default=0, verbose_name='Počet jednolůžkových pokojů'),
        ),
        migrations.AddField(
            model_name='travelpackage',
            name='number_of_suites',
            field=models.IntegerField(default=0, verbose_name='Počet apartmánů'),
        ),
        migrations.CreateModel(
            name='Prices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_date', models.DateField(blank=True, null=True, verbose_name='Datum příjezdu')),
                ('departure_date', models.DateField(blank=True, null=True, verbose_name='Datum odjezdu')),
                ('price_adult', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Cena za dospělého')),
                ('price_child', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Cena za dítě')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='viewer.hotel')),
            ],
        ),
    ]
