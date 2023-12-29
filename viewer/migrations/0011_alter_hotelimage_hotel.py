# Generated by Django 4.2.7 on 2023-12-27 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0010_hotelimage_delete_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelimage',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='images', to='viewer.hotel'),
        ),
    ]
