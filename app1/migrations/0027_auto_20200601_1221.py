# Generated by Django 3.0.6 on 2020-06-01 09:21

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app1', '0026_auto_20200529_1748'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HistoricalMeasurement',
            new_name='HistoricalMetricMeasurement',
        ),
        migrations.RenameModel(
            old_name='HistoricalValue',
            new_name='HistoricalMetricValue',
        ),
        migrations.RenameModel(
            old_name='Measurement',
            new_name='MetricMeasurement',
        ),
        migrations.RenameModel(
            old_name='Value',
            new_name='MetricValue',
        ),
        migrations.AlterModelOptions(
            name='historicalmetricmeasurement',
            options={'get_latest_by': 'history_date', 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical metric measurement'},
        ),
        migrations.AlterModelOptions(
            name='historicalmetricvalue',
            options={'get_latest_by': 'history_date', 'ordering': ('-history_date', '-history_id'), 'verbose_name': 'historical metric value'},
        ),
    ]