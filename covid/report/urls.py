from django.urls import path
from report.views import *

urlpatterns = [
    path('map/', map, name="report_map"),
    path('', main, name="report_main"),
]
