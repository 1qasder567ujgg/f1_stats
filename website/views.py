from django.shortcuts import render
from django.http import HttpResponse

from django.db.models import Sum, Count

from datetime import datetime

from .models import Seasons, \
                    Constructors, \
                    Drivers, \
                    Races, \
                    Circuits, \
                    ConstructorStandings, \
                    DriverStandings, \
                    DriverDetail, \
                    Results 

from report.staticreports.stats import getDriverCareer, \
                                        getDriverStats, \
                                        getTeamDrivers, \
                                        getTeamStats, \
                                        getDriverStandings, \
                                        getConstructorStandings, \
                                        getCircuitResults

from report.staticreports.lists import getSeasons, \
                                        getAlphabet, \
                                        getYears


def main_view(request):
    active = 'home'
    year = datetime.now().year
    context = {
                'seasons':getSeasons(),
                'active':active,
                'drivers':getDriverStandings(year)[:10],
                'teams':getConstructorStandings(year)[:10]
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
                'alink':alink
                }
    return render(request, 'website/default.html', context)
