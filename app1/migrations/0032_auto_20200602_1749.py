# Generated by Django 3.0.6 on 2020-06-02 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0031_auto_20200602_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalmetricvalue',
            name='metric_value',
            field=models.IntegerField(default=-1, verbose_name='Metric value'),
        ),
        migrations.AlterField(
            model_name='metricvalue',
            name='metric_value',
            field=models.IntegerField(default=-1, verbose_name='Metric value'),
        ),
    ]
