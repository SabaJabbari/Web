from django.db import models


class Country(models.Model):
    country_code = models.CharField(max_length=3, unique=True, verbose_name='کد کشور')
    name = models.CharField(max_length=100, verbose_name='نام کشور')
    region = models.CharField(max_length=10, verbose_name='منطقه')

    def __str__(self):
        return '{} ({})'.format(self.name, self.country_code)


class Report(models.Model):
    country = models.ForeignKey(Country, to_field='country_code', on_delete=models.CASCADE, verbose_name='کشور')

    date = models.DateField(verbose_name='تاریخ')
    new_cases = models.IntegerField(default=0, verbose_name='ابتلا جدید')
    new_deaths = models.IntegerField(default=0, verbose_name='مرگ و میر جدید')
    cumulative_cases = models.IntegerField(default=0, verbose_name='ابتلا تجمعی')
    cumulative_deaths = models.IntegerField(default=0, verbose_name='مرگ و میر تجمعی')

    type = models.ForeignKey('Type', on_delete=models.CASCADE, verbose_name='نوع')

    total_vaccinations = models.IntegerField(default=0, verbose_name='تعداد دوز تزریق شده')
    total_vaccinations_per100 = models.FloatField(default=0, verbose_name='درصد دوز تزریق شده')
    persons_fully_vaccinated = models.IntegerField(default=0, verbose_name='تعداد واکسینه کامل')
    persons_fully_vaccinated_per100 = models.FloatField(default=0, verbose_name='درصد واکسینه کامل')

    def __str__(self):
        return '{} ({}, {})'.format(self.date.isoformat, self.type, self.country.country_code)

class Type(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام')
    index = models.IntegerField(default=10, verbose_name='ترتیب')

    def __str__(self):
        return self.name
