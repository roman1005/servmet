# Generated by Django 3.0.6 on 2020-05-14 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0006_staff_table_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service_ci',
            name='design_id',
            field=models.IntegerField(default=0, unique=True),
        ),
        migrations.AlterField(
            model_name='service_ci',
            name='portfolio',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='service_ci',
            name='sub_portfolio',
            field=models.CharField(max_length=250),
        ),
    ]
