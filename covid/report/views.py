import json, datetime
from datetime import timedelta

from django.db.models import Avg
from django.shortcuts import render

from blog.models import Post
from report.models import Report, Country, Type


def main(request):
    context = {
    }
    blank_page = False
    date_get = request.GET.get("date", "")
    country_get = request.GET.get("country", "")
    type_get = int(request.GET.get("type", "1"))
    try:
        country = Country.objects.get(country_code=country_get)
        context["country"] = country_get
    except:
        blank_page = True
        context['blank_page'] = True

    try:
        date = datetime.datetime.strptime(date_get, "%Y-%m-%d").date()
        context["date"] = date_get
    except:
        blank_page = True
        context['blank_page'] = True
    try:
        type = Type.objects.get(pk=type_get)
        context["type"] = type
    except:
        blank_page = True
        context['blank_page'] = True

    countries = Country.objects.all()
    context["countries"] = countries

    types = Type.objects.all()
    context["types"] = types

    if not blank_page:
        context = tablectx(context, country, date, type)
        context = mapctx(context, date, type)
        context = chartctx(context, country, '0', type)
        context = chartctx(context, country, '1', type)
        context = chartctx(context, country, '2', type)
        context = chartctx(context, country, '3', type)
        context = chartctx(context, country, '4', type)
        context = chartctx(context, country, '5', type)
        context = blogctx(context)

    return render(request, "report/main.html", context)


def mapctx(context, date, type):
    exclude_cc = ['AS', 'XA', 'CK', 'FK', 'FO', 'GF', 'PF', 'GI', 'GP', 'GG', 'VA', 'KI', 'MV', 'MH', 'MQ', 'MU', 'YT',
                  'FM', 'MP', 'PW', 'PN', 'RE', 'XC', 'BL', 'SH', 'SC', 'XB', 'TL', 'TK', 'TV', 'WF']
    day_reports = Report.objects.filter(date=date, type=type)
    country_value = day_reports.exclude(country__country_code__in=exclude_cc)
    country_value_map = country_value.values_list('country__country_code', 'new_cases', 'cumulative_cases', 'new_deaths', 'cumulative_deaths')
    context["mapdata"] = json.dumps(list(country_value_map))
    return context


def tablectx(context, country, date, type):
    try:
        context["tabledata"] = Report.objects.filter(date=date, country=country, type=type)[0]
    except:
        context["tabledata"] = {}
        context["msg"] = "We haven't any report for this filter"
        context['blank_page'] = True
    return context


def blogctx(context):
    context["blogdata"] = Post.objects.filter(status=1)[:4]
    return context


def chartctx(context, country, type, type_):
    type_choose = ['new_cases', 'cumulative_cases', 'new_deaths', 'cumulative_deaths', 'total_vaccinations', 'persons_fully_vaccinated']
    chart_setting = {
                        0: {'name': "New Cases", 'color': '#008ebc'},
                        1: {'name': "Cumulative Cases", 'color': '#008ebc'},
                        2: {'name': "New Deaths", 'color': '#bb551b'},
                        3: {'name': "Cumulative Deaths", 'color': '#bb551b'},
                        4: {'name': "Total Vaccinations", 'color': '#08732d'},
                        5: {'name': "Persons Fully Vaccinated", 'color': '#08732d'}
                     }
    try:
        from_date = Report.objects.filter(country=country, type=type_).order_by('date')[0].date
        to_date = Report.objects.filter(country=country, type=type_).order_by('-date')[0].date

        time_step = 7
        report = Report.objects.filter(country=country, type=type_)

        # chart_data = [['date', 'Single Ticket Count', 'Group Ticket Count']]
        chart_data = []

        date1 = to_date - timedelta(days=364)
        date2 = to_date
        step = timedelta(int(time_step))
        curr = date1
        while curr < date2:
            start = curr
            end = curr + step
            step_title = end.strftime('%b %d')
            print(curr)
            reports_step = report.filter(date__gte=start).filter(date__lt=end)

            data = reports_step.aggregate(Avg(type_choose[int(type)]))
            chart_data.append([step_title, round(data[type_choose[int(type)]+'__avg'])])
            curr += step
        context['chart'+type+'_title'] = type_choose[int(type)]
        context['chart'+type+'data'] = chart_data
        context['chart_setting'] = chart_setting
        # return chart_data
    except:
        context["msg"] = "We haven't any report for this filter"
        context['blank_page'] = True
    return context



def map(request, type):
    exclude_cc = ['AS', 'XA', 'CK', 'FK', 'FO', 'GF', 'PF', 'GI', 'GP', 'GG', 'VA', 'KI', 'MV', 'MH', 'MQ', 'MU', 'YT',
                  'FM', 'MP', 'PW', 'PN', 'RE', 'XC', 'BL', 'SH', 'SC', 'XB', 'TL', 'TK', 'TV', 'WF']
    date = datetime.date(2022, 3, 17)
    day_reports = Report.objects.filter(date=date, type=type)
    country_value = day_reports.exclude(country__country_code__in=exclude_cc)
    country_value_map = country_value.values_list('country__country_code', 'cumulative_cases')
    context = {
        "mapdata": json.dumps(list(country_value_map)),
        # "mapdata_min": country_value.aggregate(Min('cumulative_cases'))['cumulative_cases__min'],
        # "mapdata_max": country_value.aggregate(Max('cumulative_cases'))['cumulative_cases__max'],
    }
    # context["mapdata_interval"] = round(context["mapdata_max"]/20)
    return render(request, "report/map.html", context)
