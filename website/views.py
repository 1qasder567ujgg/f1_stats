from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Sum
from .models import Seasons, Constructors, Drivers, Races, ConstructorStandings, DriverStandings, DriverDetail, Results

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
    driver = Drivers.objects.get(driverid=int(id))
    points = Results.objects.filter(driverid=int(id)).aggregate(Sum('points'))['points__sum']
    active = 'driver'
    letters = [chr(i) for i in range(65, 91)]
    letter = driver.surname[0]
    alink = 'drivers'
    # driverDetail = DriverDetail.objects.get(id=int(id))
    context = {
                'active':active,
                'driver':driver,
                'points':points,
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
