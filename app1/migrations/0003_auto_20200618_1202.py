# Generated by Django 3.0.6 on 2020-06-18 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_auto_20200618_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalmetric',
            name='design_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='metric',
            name='design_id',
            field=models.IntegerField(default=0),
        ),
    ]
