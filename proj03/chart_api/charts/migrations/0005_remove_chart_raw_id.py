# Generated by Django 4.1.3 on 2022-12-05 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0004_alter_chart_asst_txt_let_cnt_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chart',
            name='raw_id',
        ),
    ]
