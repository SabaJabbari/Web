# Generated by Django 4.0.3 on 2022-03-21 09:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_code', models.CharField(max_length=3, unique=True, verbose_name='کد کشور')),
                ('name', models.CharField(max_length=100, verbose_name='نام کشور')),
                ('region', models.CharField(max_length=10, verbose_name='منطقه')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='تاریخ')),
                ('new_cases', models.IntegerField(verbose_name='ابتلا جدید')),
                ('new_deaths', models.IntegerField(verbose_name='مرگ و میر جدید')),
                ('cumulative_cases', models.IntegerField(verbose_name='ابتلا تجمعی')),
                ('cumulative_deaths', models.IntegerField(verbose_name='مرگ و میر تجمعی')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='report.country', verbose_name='کشور')),
            ],
        ),
    ]
