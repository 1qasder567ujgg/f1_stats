"""f1_stats URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from website import views as web

urlpatterns = [
    url(r'^$', web.main_view, name='main_view'),
    url(r'^driver/(?P<id>[\w+]+)$', web.driver_view, name='driver_view'),
    url(r'^drivers/(?P<letter>[A-Z]{1})$', web.drivers_view, name='drivers_view'),
    url(r'^team/(?P<id>[\w+]+)$', web.team_view, name='team_view'),
    url(r'^teams/(?P<letter>[A-Z]{1})$', web.teams_view, name='teams_view'),
    url(r'^circuit/(?P<id>[\w+]+)$', web.circuit_view, name='circuit_view'),
    url(r'^circuits/(?P<letter>[A-Z]{1})$', web.circuits_view, name='circuits_view'),
    url(r'^season/(?P<year>[\w+]+)$', web.season_view, name='season_view'),
    url(r'^reports/', web.reports_view, name='reports_view'),
    url(r'^report/(?P<id>[\w+]+)$', web.report_view, name='report_view'),
    url(r'^admin/', admin.site.urls),
]
