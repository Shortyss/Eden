# Generated by Django 4.2.7 on 2024-01-17 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0030_remove_purchase_travelers_purchase_traveler'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='traveler',
        ),
        migrations.AddField(
            model_name='purchase',
            name='traveler',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='travelers_purchase', to='viewer.traveler', verbose_name='Cestující'),
        ),
    ]
