# Generated by Django 4.1.3 on 2022-12-07 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0005_remove_chart_raw_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='chart',
            name='CHART_CD',
            field=models.CharField(blank=True, max_length=33, null=True),
        ),
        migrations.AddField(
            model_name='chart',
            name='CHART_TPCD',
            field=models.CharField(blank=True, max_length=33, null=True),
        ),
    ]
