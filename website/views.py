from django.shortcuts import render
from django.http import HttpResponse

from django.db.models import Sum, Count

from .models import Seasons, Constructors, Drivers, Races, ConstructorStandings, DriverStandings, DriverDetail, Results
from report.models import DriverStats, DriverCareer, TeamStats, TeamDrivers


def main_view(request):
    seasons = Seasons.objects.all().order_by('-year')
    active = 'home'
    lastRace = DriverStandings.objects.all().order_by('-raceid')[0]
    driverPoints = DriverStandings.objects.all().filter(raceid=lastRace.raceid).order_by('-points')[:10]
    constructorPoints = ConstructorStandings.objects.all().filter(raceid=lastRace.raceid).order_by('-points')[:10]
    context = {
                'seasons':seasons,
                'active':active,
                'driverPoints':driverPoints,
                'constructorPoints':constructorPoints,
                }
    return render(request, 'website/default.html', context)


def driver_view(request, id):
    driverid = int(id)
    driver = Drivers.objects.get(driverid=driverid)
    stats = DriverStats()
    stats.getStats(driverid)
    career = DriverCareer()
    career = career.getCareer(driverid)
    active = 'driver'
    letters = [chr(i) for i in range(65, 91)]
    letter = driver.surname[0]
    alink = 'drivers'
    # driverDetail = DriverDetail.objects.get(id=int(id))
    context = {
                'active':active,
                'driver':driver,
                'stats':stats,
                'career':career,
                'letters':letters,
                'letter':letter,
                'alink':alink
                }
    return render(request, 'website/default.html', context)


def drivers_view(request, letter):
    drivers = Drivers.objects.filter(surname__startswith=letter).order_by('surname')
    active = 'drivers'
    letters = [chr(i) for i in range(65, 91)]
    alink = 'drivers'
    context = {
                'active':active,
                'drivers':drivers,
                'letters':letters,
                'letter':letter,
                'alink':alink
                }
    return render(request, 'website/default.html', context)


def team_view(request, id):
    teamid = int(id)
    team = Constructors.objects.get(constructorid=teamid)
    stats = TeamStats()
    stats.getStats(teamid)
    drivers = TeamDrivers()
    drivers = drivers.getDrivers(teamid)
    active = 'team'
    letters = [chr(i) for i in range(65, 91)]
    letter = team.name[0]
    alink = 'teams'
    # driverDetail = DriverDetail.objects.get(id=int(id))
    context = {
                'active':active,
                'team':team,
                'stats':stats,
                'drivers':drivers,
                'letters':letters,
                'letter':letter,
                'alink':alink
                }
    return render(request, 'website/default.html', context)


def teams_view(request, letter):
    teams = Constructors.objects.filter(name__startswith=letter).order_by('name')
    active = 'teams'
    letters = [chr(i) for i in range(65, 91)]
    alink = 'teams'
    context = {
                'active':active,
                'teams':teams,
                'letters':letters,
                'letter':letter,
                'alink':alink
                }
    return render(request, 'website/default.html', context)
