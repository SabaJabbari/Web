# Generated by Django 4.0.3 on 2022-06-26 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0006_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='report.type', verbose_name='نوع'),
        ),
    ]