# Generated by Django 4.0.3 on 2022-06-26 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0007_report_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.type', verbose_name='نوع'),
        ),
    ]