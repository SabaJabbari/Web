from django.contrib import admin
from django.core import serializers
import json
from report.automate import covid19, aids
from report.models import *


class CountryAdmin(admin.ModelAdmin):
    list_display = ['country_code', 'name', 'region']
    search_fields = ['country_code', 'name', 'region']


admin.site.register(Country, CountryAdmin)


@admin.action(description='Reports will be updated(Covid-19)')
def reports_update(modeladmin, request, queryset):
    covid19()

@admin.action(description='Reports will be updated(Flumart)')
def reports_update2(modeladmin, request, queryset):
    flumart()

@admin.action(description='Reports will be updated(AIDS)')
def reports_update3(modeladmin, request, queryset):
    qs_json = serializers.serialize('json', queryset)
    qs_json = json.loads(qs_json)
    country = Country.objects.filter(country_code=qs_json[0]['fields']['country'])[0]
    aids(str(country.name))

class ReportAdmin(admin.ModelAdmin):
    list_display = ['date', 'country', 'new_cases', 'new_deaths', 'cumulative_cases', 'cumulative_deaths', 'persons_fully_vaccinated', 'persons_fully_vaccinated_per100', 'total_vaccinations', 'total_vaccinations_per100']
    search_fields = ['date', 'country__country_code']
    list_filter = ['type', 'country']
    actions = [reports_update, reports_update2, reports_update3]


admin.site.register(Report, ReportAdmin)


class TypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'index']
    search_fields = ['name']

admin.site.register(Type, TypeAdmin)
