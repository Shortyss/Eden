# Generated by Django 4.2.7 on 2024-01-25 11:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0041_traveler_purchase'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='traveler',
            name='purchase',
        ),
        migrations.AddField(
            model_name='purchase',
            name='traveler',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='viewer.traveler'),
        ),
    ]
