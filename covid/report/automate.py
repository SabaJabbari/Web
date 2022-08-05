from datetime import datetime, date, timedelta
import pandas as pd
from report.crawler import get_flumart_excel
from report.models import Report, Country
import random

def aids(country_name):
    url = 'https://corgis-edu.github.io/corgis/datasets/csv/aids/aids.csv'
    df = pd.read_csv(url, sep=',')
    for it in range(1780, df.shape[0]):
        CN_selected = str(df.iloc[it, 0])
        if CN_selected.lower() != country_name.lower():
            continue
        country_obj = Country.objects.filter(name=CN_selected)
        if country_obj.exists():
            year_selected = int(df.iloc[it, 1])
            deaths_of_year = int(df.iloc[it, 4])
            cases_of_year = int(df.iloc[it, 15])
            deaths_dtd_val = deaths_of_year / 365
            cases_dtd_val = cases_of_year / 365
            random_min = cases_dtd_val * -0.1
            random_max = cases_dtd_val * 0.1
            cumulative_cases = 0
            cumulative_deaths = 0
            for dayofyear in range(1, 367):
                date = datetime(year_selected, 1, 1) + timedelta(days=dayofyear - 1)
                random_num = round(random.uniform(random_min, random_max))
                new_cases_dtd = cases_dtd_val + random_num
                new_deaths_dtd = deaths_dtd_val + random_num
                new_cases_dtd = round(new_cases_dtd, 1) if new_cases_dtd < 1 else new_cases_dtd
                new_deaths_dtd = round(new_deaths_dtd, 1) if new_deaths_dtd < 1 else new_deaths_dtd
                Report.objects.create(country=country_obj[0], date=date, type_id=3, new_cases=new_cases_dtd, cumulative_cases=cumulative_cases, new_deaths=new_deaths_dtd, cumulative_deaths=cumulative_deaths)


def covid19():
    url = 'https://covid19.who.int/WHO-COVID-19-global-data.csv'
    df = pd.read_csv(url, sep=',')
    for it in range(0, df.shape[0]):
        Date_selected = str(df.iloc[it, 0])
        CC_selected = str(df.iloc[it, 1])
        if not Report.objects.filter(date__exact=Date_selected, country__country_code=CC_selected).exists():
            country = Country.objects.get(country_code=CC_selected)
            new_cases = int(df.iloc[it, 4])
            cumulative_cases = int(df.iloc[it, 5])
            new_deaths = int(df.iloc[it, 6])
            cumulative_deaths = int(df.iloc[it, 7])
            Report.objects.create(country=country, date=datetime.fromisoformat(Date_selected).date(), type_id=1, new_cases=new_cases, cumulative_cases=cumulative_cases, new_deaths=new_deaths, cumulative_deaths=cumulative_deaths)


def goto_top_row(df, i, j):
    value = df.iloc[i, j]
    row = i
    while str(value) == 'nan':
        row -= 1
        value = df.iloc[row, j]
    return row


#def flumart():
#    for country_code in range(0, 10):
 #       file_path = get_flumart_excel(country_code)
  #      df = pd.read_excel(file_path)
   #     for it in range(7, df.shape[0]):
    #        country_selected = str(df.iloc[goto_top_row(df, it, 1), 1])
     #       country_obj = Country.objects.filter(name__exact=country_selected)[0]
      #      year_selected = int(df.iloc[goto_top_row(df, it, 2), 2])
       #     week_selected = int(df.iloc[it, 3])
        #    if str(df.iloc[it, 63]) == 'nan' or str(df.iloc[it, 79]) == 'nan':
         #       continue
         #   SARI_cases = float(df.iloc[it, 63])
          #  SARI_deaths = float(df.iloc[it, 79])
           # SARI_cases_dtd = round(SARI_cases/7)
            #SARI_deaths_dtd = round(SARI_deaths/7)

           # for i in range(1, 8):  # generate days of week
            #    report_date = date.fromisocalendar(year_selected, week_selected, i)  # (year, week, day of week)
             #   if not Report.objects.filter(date__exact=report_date, country=country_obj).exists():
              #      new_cases = SARI_cases_dtd
               #     cumulative_cases = 0
                #    new_deaths = SARI_deaths_dtd
                 #   cumulative_deaths = 0
                  #  Report.objects.create(country=country_obj, date=report_date, type_id=2,
                   #                       new_cases=new_cases, cumulative_cases=cumulative_cases, new_deaths=new_deaths,
                    #                      cumulative_deaths=cumulative_deaths)#


