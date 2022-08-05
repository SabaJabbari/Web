# Generated by Django 4.0.3 on 2022-06-26 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0005_report_persons_fully_vaccinated_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='نام')),
                ('index', models.IntegerField(default=10, verbose_name='ترتیب')),
            ],
        ),
    ]