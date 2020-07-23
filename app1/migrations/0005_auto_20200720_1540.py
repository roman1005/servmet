# Generated by Django 3.0.6 on 2020-07-20 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0004_auto_20200720_1405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalmetric',
            name='status',
            field=models.CharField(choices=[('Defined', 'Defined'), ('Submited', 'Submited'), ('Deployed', 'Deployed'), ('Operational', 'Operational'), ('Retired(Upgrade)', 'Retired(Upgrade)'), ('Retired(Replacemenet)', 'Retired(Replacemenet)'), ('Retired(Obsolete)', 'Retired(Obsolete)'), ('Cancelled(Upgrade)', 'Cancelled(Upgrade)'), ('Cancelled(Replacemenet)', 'Cancelled(Replacemenet)'), ('External premises', 'External premises'), ('Under consideration', 'Under consideration'), ('Unknown', 'Unknown'), ('Displaced', 'Displaced'), ('Not agreed', 'Not agreed')], default='DEF', max_length=40),
        ),
        migrations.AlterField(
            model_name='historicalservice',
            name='status',
            field=models.CharField(choices=[('Defined', 'Defined'), ('Submited', 'Submited'), ('Deployed', 'Deployed'), ('Operational', 'Operational'), ('Retired(Upgrade)', 'Retired(Upgrade)'), ('Retired(Replacemenet)', 'Retired(Replacemenet)'), ('Retired(Obsolete)', 'Retired(Obsolete)'), ('Cancelled(Upgrade)', 'Cancelled(Upgrade)'), ('Cancelled(Replacemenet)', 'Cancelled(Replacemenet)'), ('External premises', 'External premises'), ('Under consideration', 'Under consideration'), ('Unknown', 'Unknown'), ('Displaced', 'Displaced'), ('Not agreed', 'Not agreed')], default='Defined', max_length=40),
        ),
        migrations.AlterField(
            model_name='metric',
            name='status',
            field=models.CharField(choices=[('Defined', 'Defined'), ('Submited', 'Submited'), ('Deployed', 'Deployed'), ('Operational', 'Operational'), ('Retired(Upgrade)', 'Retired(Upgrade)'), ('Retired(Replacemenet)', 'Retired(Replacemenet)'), ('Retired(Obsolete)', 'Retired(Obsolete)'), ('Cancelled(Upgrade)', 'Cancelled(Upgrade)'), ('Cancelled(Replacemenet)', 'Cancelled(Replacemenet)'), ('External premises', 'External premises'), ('Under consideration', 'Under consideration'), ('Unknown', 'Unknown'), ('Displaced', 'Displaced'), ('Not agreed', 'Not agreed')], default='DEF', max_length=40),
        ),
        migrations.AlterField(
            model_name='service',
            name='status',
            field=models.CharField(choices=[('Defined', 'Defined'), ('Submited', 'Submited'), ('Deployed', 'Deployed'), ('Operational', 'Operational'), ('Retired(Upgrade)', 'Retired(Upgrade)'), ('Retired(Replacemenet)', 'Retired(Replacemenet)'), ('Retired(Obsolete)', 'Retired(Obsolete)'), ('Cancelled(Upgrade)', 'Cancelled(Upgrade)'), ('Cancelled(Replacemenet)', 'Cancelled(Replacemenet)'), ('External premises', 'External premises'), ('Under consideration', 'Under consideration'), ('Unknown', 'Unknown'), ('Displaced', 'Displaced'), ('Not agreed', 'Not agreed')], default='Defined', max_length=40),
        ),
    ]