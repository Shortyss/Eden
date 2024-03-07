# Generated by Django 4.2.7 on 2024-02-22 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0052_alter_city_country_alter_city_island_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airport',
            name='airport_city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='viewer.city', verbose_name='Město'),
        ),
        migrations.AlterField(
            model_name='city',
            name='country',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='viewer.country', verbose_name='Stát'),
        ),
        migrations.AlterField(
            model_name='city',
            name='island',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='viewer.island', verbose_name='Ostrov'),
        ),
        migrations.AlterField(
            model_name='country',
            name='continent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='viewer.continent', verbose_name='Kontinent'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hotels_of_cities', to='viewer.city', verbose_name='Město'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='city_of_country', to='viewer.country', verbose_name='Stát'),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='transportation',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transportation_of_hotel', to='viewer.transportation', verbose_name='Doprava'),
        ),
        migrations.AlterField(
            model_name='island',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cities', to='viewer.country', verbose_name='Stát'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='hotel',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchase_hotel', to='viewer.hotel'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='meal_plan',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='travel_packages', to='viewer.mealplan', verbose_name='Strava'),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='transportation',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='purchase_transportation', to='viewer.transportation', verbose_name='Doprava'),
        ),
        migrations.AlterField(
            model_name='transportation',
            name='arrival_airport',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arrival_transportation', to='viewer.airport', verbose_name='Letiště příletu'),
        ),
        migrations.AlterField(
            model_name='transportation',
            name='departure_airport',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='departure_transportation', to='viewer.airport', verbose_name='Letiště odletu'),
        ),
    ]