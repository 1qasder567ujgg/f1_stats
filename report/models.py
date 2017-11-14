from django.db import models, connection

from django.db.models import Sum, Count, Min

from website.models import Drivers, Results, Laptimes, Qualifying, Constructors


class DriverStats(models.Model):
    driver = models.ForeignKey(Drivers)
    points = models.FloatField()
    races = models.IntegerField()
    wins = models.IntegerField()
    podiums = models.IntegerField()
    lapst = models.IntegerField()
    lapsf = models.IntegerField()
    lapsl = models.IntegerField()
    champion = models.IntegerField()
    poles = models.IntegerField()
    bestq = models.IntegerField()
    bestr = models.IntegerField()

    class Meta:
        managed = False


    def getStats(self, driverid):
        driverid = int(driverid)
        self.points = Results.objects.filter(driverid=driverid).aggregate(Sum('points'))['points__sum']
        self.races = Results.objects.filter(driverid=driverid).aggregate(Count('raceid'))['raceid__count']
        self.wins = Results.objects.filter(driverid=driverid, position=1).aggregate(Count('raceid'))['raceid__count']
        self.podiums = Results.objects.filter(driverid=driverid, position__lte=3).aggregate(Count('raceid'))['raceid__count']
        self.lapst = Results.objects.filter(driverid=driverid).aggregate(Sum('laps'))['laps__sum']
        self.lapsf = Results.objects.filter(driverid=driverid, rank=1).aggregate(Count('raceid'))['raceid__count']
        self.lapsl = Laptimes.objects.filter(driverid=driverid, position=1).aggregate(Count('lap'))['lap__count']
        self.champion = 0
        self.poles = Qualifying.objects.filter(driverid=driverid, position=1).aggregate(Count('position'))['position__count']
        self.bestq = Qualifying.objects.filter(driverid=driverid).aggregate(Min('position'))['position__min']
        self.bestr = Results.objects.filter(driverid=driverid).aggregate(Min('position'))['position__min']


class DriverCareer(models.Model):

    def getCareer(self, driverid):
        with connection.cursor() as cursor:
            cursor.execute('SELECT rs.year, c.name, r.constructorId \
                            FROM f1db.results r \
                            INNER JOIN f1db.constructors c ON c.constructorId = r.constructorId \
                            INNER JOIN f1db.races rs ON rs.raceId = r.raceId \
                            WHERE r.driverId = %s \
                            GROUP BY rs.year, c.name \
                            ORDER BY rs.year, c.name', [str(int(driverid))])
            row = cursor.fetchall()
        return row


class TeamStats(models.Model):
    driver = models.ForeignKey(Drivers)
    points = models.FloatField()
    races = models.IntegerField()
    wins = models.IntegerField()
    podiums = models.IntegerField()
    lapst = models.IntegerField()
    lapsf = models.IntegerField()
    lapsl = models.IntegerField()
    champion = models.IntegerField()
    poles = models.IntegerField()
    bestq = models.IntegerField()
    bestr = models.IntegerField()

    class Meta:
        managed = False


    def getStats(self, teamid):
        teamid = int(teamid)
        self.points = round(Results.objects.filter(constructorid=teamid).aggregate(Sum('points'))['points__sum'], 2)
        self.races = Results.objects.filter(constructorid=teamid).aggregate(Count('raceid'))['raceid__count']
        self.wins = Results.objects.filter(constructorid=teamid, position=1).aggregate(Count('raceid'))['raceid__count']
        self.podiums = Results.objects.filter(constructorid=teamid, position__lte=3).aggregate(Count('raceid'))['raceid__count']
        self.lapst = Results.objects.filter(constructorid=teamid).aggregate(Sum('laps'))['laps__sum']
        self.lapsf = Results.objects.filter(constructorid=teamid, rank=1).aggregate(Count('raceid'))['raceid__count']
        self.lapsl =  0 # Laptimes.objects.filter(constructorid=teamid, position=1).aggregate(Count('lap'))['lap__count']
        self.champion = 0
        self.poles = Qualifying.objects.filter(constructorid=teamid, position=1).aggregate(Count('position'))['position__count']
        self.bestq = Qualifying.objects.filter(constructorid=teamid).aggregate(Min('position'))['position__min']
        self.bestr = Results.objects.filter(constructorid=teamid).aggregate(Min('position'))['position__min']


class TeamDrivers(models.Model):

    def getDrivers(self, teamid):
        with connection.cursor() as cursor:
            cursor.execute('SELECT rs.year, d.forename, d.surname, r.driverId \
                            FROM f1db.results r \
                            INNER JOIN f1db.drivers d ON d.driverId = r.driverId \
                            INNER JOIN f1db.races rs ON rs.raceId = r.raceId \
                            WHERE r.constructorId = %s \
                            GROUP BY rs.year, r.driverId, d.forename, d.surname \
                            ORDER BY rs.year, d.surname, d.forename', [str(int(teamid))])
            row = cursor.fetchall()
        return row        
