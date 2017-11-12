from django.shortcuts import render
from django.http import HttpResponse
from .models import Seasons, Constructors, Drivers, Races, ConstructorStandings, DriverStandings

# Create your views here.
def main_view(request):
    seasons = Seasons.objects.all().order_by('-year')
    active = 'Home'
    lastRace = DriverStandings.objects.all().order_by('-raceid')[0]
    driverPoints = DriverStandings.objects.all().filter(raceid=lastRace.raceid).order_by('-points')[:10]
    constructorPoints = ConstructorStandings.objects.all().filter(raceid=lastRace.raceid).order_by('-points')[:10]

    return render(request, 'website/home.html', {
                                                'seasons':seasons,
                                                'active':active,
                                                'driverPoints':driverPoints,
                                                'constructorPoints':constructorPoints,
                                                })