# Generated by Django 3.0.6 on 2020-05-22 07:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_auto_20200521_0959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalstaff',
            name='surname',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='service',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customerID', to='app1.Staff'),
        ),
        migrations.AlterField(
            model_name='service',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ownerID', to='app1.Staff'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='surname',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]