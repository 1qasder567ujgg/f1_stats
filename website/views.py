from django.shortcuts import render
from django.http import HttpResponse

from django.db.models import Sum, Count

from datetime import datetime

import f1_stats.other_settings as other

from .models import Seasons, \
                    Constructors, \
                    Drivers, \
                    Races, \
                    Circuits, \
                    ConstructorStandings, \
                    DriverStandings, \
                    DriverDetail, \
                    Results 

from report.models import Reports

from forecast.models import Forecast

from report.staticreports.stats import getDriverCareer, \
                                        getDriverStats, \
                                        getTeamDrivers, \
                                        getTeamStats, \
                                        getDriverStandings, \
                                        getConstructorStandings, \
                                        getCircuitResults

from report.staticreports.lists import getSeasons, \
                                        getAlphabet, \
                                        getYears, \
                                        getReports, \
                                        getMonacoWeather

from report.staticreports.reports import getTotalWins, \
                                        getTotalPoints, \
                                        getTotalParticipants ,\
                                        getMonacoLapTime, \
                                        getTotalCareer, \
                                        getPitstopTime


def main_view(request):
    raceForecast = Forecast.objects.all().order_by('position')[:3]
    qualForecast = Forecast.objects.all().order_by('grid')[:3]
    active = 'home'
    year = datetime.now().year
    context = {
                'seasons':getSeasons(),
                'active':active,
                'drivers':getDriverStandings(year)[:10],
                'teams':getConstructorStandings(year)[:10],
                'raceForecast':raceForecast,
                'qualForecast':qualForecast,
                }
    return render(request, 'website/default.html', context)


def driver_view(request, id):
    driverid = int(id)
    driver = Drivers.objects.get(driverid=driverid)
    stats = getDriverStats(driverid)
    career = getDriverCareer(driverid)
    active = 'driver'
    letter = driver.surname[0]
    alink = 'drivers'
    context = {
                'seasons':getSeasons(),
                'active':active,
                'driver':driver,
                'stats':stats,
                'career':career,
                'reflist':getAlphabet(),
                'selected':letter,
                'alink':alink
                }
    return render(request, 'website/default.html', context)


def drivers_view(request, letter):
    drivers = Drivers.objects.filter(surname__startswith=letter).order_by('surname')
    active = 'drivers'
    alink = 'drivers'
    context = {
                'seasons':getSeasons(),
                'active':active,
                'drivers':drivers,
                'reflist':getAlphabet(),
                'selected':letter,
                'alink':alink
                }
    return render(request, 'website/default.html', context)


def team_view(request, id):
    teamid = int(id)
    team = Constructors.objects.get(constructorid=teamid)
    stats = getTeamStats(teamid)
    drivers = getTeamDrivers(teamid)
    active = 'team'
    letter = team.name[0]
    alink = 'teams'
    context = {
                'seasons':getSeasons(),
                'active':active,
                'team':team,
                'stats':stats,
                'drivers':drivers,
                'reflist':getAlphabet(),
                'selected':letter,
                'alink':alink
                }
    return render(request, 'website/default.html', context)


def teams_view(request, letter):
    teams = Constructors.objects.filter(name__startswith=letter).order_by('name')
    active = 'teams'
    alink = 'teams'
    context = {
                'seasons':getSeasons(),
                'active':active,
                'teams':teams,
                'reflist':getAlphabet(),
                'selected':letter,
                'alink':alink
                }
    return render(request, 'website/default.html', context)


def season_view(request, year):
    year = int(year)
    active = 'seasons'
    alink = 'season'
    context = {
                'drivers':getDriverStandings(year),
                'teams':getConstructorStandings(year),
                'seasons':getSeasons(),
                'active':active,
                'reflist':getYears(),
                'selected':year,
                'alink':alink
                }
    return render(request, 'website/default.html', context)


def circuits_view(request, letter):
    circuits = Circuits.objects.filter(name__startswith=letter).order_by('name')
    active = 'circuits'
    alink = 'circuits'
    context = {
                'seasons':getSeasons(),
                'active':active,
                'circuits':circuits,
                'reflist':getAlphabet(),
                'selected':letter,
                'alink':alink
                }
    return render(request, 'website/default.html', context)


def circuit_view(request, id):
    circuitid = int(id)
    circuit = Circuits.objects.get(circuitid=circuitid)
    drivers = getCircuitResults(circuitid)
    active = 'circuit'
    letter = circuit.name[0]
    alink = 'circuits'
    context = {
                'seasons':getSeasons(),
                'active':active,
                'circuit':circuit,
                'drivers':drivers,
                'reflist':getAlphabet(),
                'selected':letter,
                'alink':alink,
                'mapkey':other.BING_MAP_KEY
                }
    return render(request, 'website/default.html', context)


def reports_view(request):
    reports = Reports.objects.all()
    active = 'reports'
    alink = 'reports'
    context = {
                'seasons':getSeasons(),
                'reports':reports,
                'active':active,
                'alink':alink
                }
    return render(request, 'website/default.html', context)


def report_view(request, id):
    reportid = int(id)
    reports = Reports.objects.all()
    report = Reports.objects.get(id=reportid)

    if report.methodname == 'getTotalWins':
        data = getTotalWins()
        labels = []
        weather = []
    elif report.methodname == 'getTotalPoints':
        data = getTotalPoints()
        labels = []
        weather = []
    elif report.methodname == 'getTotalParticipants':
        rep = getTotalParticipants()
        labels = [d[0] for d in rep]
        teams = [d[1] for d in rep]
        drivers = [d[2] for d in rep]
        data = [teams, drivers]
        weather = []
    elif report.methodname == 'getMonacoLapTime':
        rep = getMonacoLapTime()
        labels = [d[0] for d in rep]
        race = [d[1]/1000 for d in rep]
        qual = [min([d[2], d[3], d[4]])/1000 for d in rep]
        print(rep)
        weather = getMonacoWeather()
        data = [race, qual]
    elif report.methodname == 'getTotalCareer':
        data = getTotalCareer()
        labels = []
        weather = []
    elif report.methodname == 'getPitstopTime':
        # r.year, MinTime, AvgTime
        circuitid = 6 # Monaco
        rep = getPitstopTime(circuitid) 
        labels = [d[0] for d in rep]
        cmin = [d[1]/1000 for d in rep]
        cavg = [d[2]/1000 for d in rep]
        circuit1 = [cmin, cavg]

        circuitid = 4 # Spain
        rep = getPitstopTime(circuitid) 
        cmin = [d[1]/1000 for d in rep]
        cavg = [d[2]/1000 for d in rep]
        circuit2 = [cmin, cavg]
        
        circuitid = 9 # Spa
        rep = getPitstopTime(circuitid) 
        cmin = [d[1]/1000 for d in rep]
        cavg = [d[2]/1000 for d in rep]
        circuit3 = [cmin, cavg]

        weather = []
        data = [circuit1, circuit2, circuit3]
    else:
        data = []
        labels = []
        weather = []

    active = 'report'
    alink = 'reports'
    context = {
                'seasons':getSeasons(),
                'reports':reports,
                'weather':weather,
                'active':active,
                'data':data,
                'labels':labels,
                'selected':reportid,
                'header':report.name,
                'alink':alink
                }
    return render(request, 'website/default.html', context)


def forecast_view(request):
    raceForecast = Forecast.objects.all().order_by('position')
    qualForecast = Forecast.objects.all().order_by('grid')
    nextRace = Races.objects.get(raceid=985)
    year = datetime.now().year
    active = 'forecast'
    context = {
                'seasons':getSeasons(),
                'active':active,
                'raceForecast':raceForecast,
                'qualForecast':qualForecast,
                'race':nextRace,
                'drivers':getDriverStandings(year)[:10],
                'teams':getConstructorStandings(year)[:10]
                }
    return render(request, 'website/default.html', context)
