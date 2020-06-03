# Generated by Django 3.0.6 on 2020-06-02 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0028_auto_20200602_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalmetric',
            name='measr_regularity',
            field=models.CharField(default='', max_length=100, verbose_name='Measure Regularity'),
        ),
        migrations.AlterField(
            model_name='historicalmetric',
            name='publ_deadline',
            field=models.CharField(default='', max_length=100, verbose_name='Publication Deadline'),
        ),
        migrations.AlterField(
            model_name='historicalmetric',
            name='publ_regularity',
            field=models.CharField(default='', max_length=100, verbose_name='Publication Regularity'),
        ),
        migrations.AlterField(
            model_name='metric',
            name='measr_regularity',
            field=models.CharField(default='', max_length=100, verbose_name='Measure Regularity'),
        ),
        migrations.AlterField(
            model_name='metric',
            name='publ_deadline',
            field=models.CharField(default='', max_length=100, verbose_name='Publication Deadline'),
        ),
        migrations.AlterField(
            model_name='metric',
            name='publ_regularity',
            field=models.CharField(default='', max_length=100, verbose_name='Publication Regularity'),
        ),
    ]