from django.db import connection
from django.db.models import Sum, Count, Min

from website.models import Drivers, Results, Laptimes, Qualifying, Constructors

def getDriverCareer(driverid):
    with connection.cursor() as cursor:
        cursor.execute('SELECT rs.year, c.name, r.constructorId \
                        FROM f1db.results r \
                        INNER JOIN f1db.constructors c ON c.constructorId = r.constructorId \
                        INNER JOIN f1db.races rs ON rs.raceId = r.raceId \
                        WHERE r.driverId = %s \
                        GROUP BY rs.year, c.name \
                        ORDER BY rs.year, c.name', [str(int(driverid))])
        career = cursor.fetchall()
    return career


def getDriverStats(driverid):
    driverid = int(driverid)
    stats = dict()
    stats['points'] = Results.objects.filter(driverid=driverid).aggregate(Sum('points'))['points__sum']
    stats['races'] = Results.objects.filter(driverid=driverid).aggregate(Count('raceid'))['raceid__count']
    stats['wins'] = Results.objects.filter(driverid=driverid, position=1).aggregate(Count('raceid'))['raceid__count']
    stats['podiums'] = Results.objects.filter(driverid=driverid, position__lte=3).aggregate(Count('raceid'))['raceid__count']
    stats['lapst'] = Results.objects.filter(driverid=driverid).aggregate(Sum('laps'))['laps__sum']
    stats['lapsf'] = Results.objects.filter(driverid=driverid, rank=1).aggregate(Count('raceid'))['raceid__count']
    stats['lapsl'] = Laptimes.objects.filter(driverid=driverid, position=1).aggregate(Count('lap'))['lap__count']
    stats['poles'] = Qualifying.objects.filter(driverid=driverid, position=1).aggregate(Count('position'))['position__count']
    stats['bestq'] = Qualifying.objects.filter(driverid=driverid).aggregate(Min('position'))['position__min']
    stats['bestr'] = Results.objects.filter(driverid=driverid).aggregate(Min('position'))['position__min']
    return stats


def getTeamDrivers(teamid):
    with connection.cursor() as cursor:
        cursor.execute('SELECT rs.year, d.forename, d.surname, r.driverId \
                        FROM f1db.results r \
                        INNER JOIN f1db.drivers d ON d.driverId = r.driverId \
                        INNER JOIN f1db.races rs ON rs.raceId = r.raceId \
                        WHERE r.constructorId = %s \
                        GROUP BY rs.year, r.driverId, d.forename, d.surname \
                        ORDER BY rs.year, d.surname, d.forename', [str(int(teamid))])
        drivers = cursor.fetchall()
    return drivers       


def getTeamStats(teamid):
    teamid = int(teamid)
    stats = dict()
    stats['points'] = round(Results.objects.filter(constructorid=teamid).aggregate(Sum('points'))['points__sum'], 2)
    stats['races'] = Results.objects.filter(constructorid=teamid).aggregate(Count('raceid'))['raceid__count']
    stats['wins'] = Results.objects.filter(constructorid=teamid, position=1).aggregate(Count('raceid'))['raceid__count']
    stats['podiums'] = Results.objects.filter(constructorid=teamid, position__lte=3).aggregate(Count('raceid'))['raceid__count']
    stats['lapst'] = Results.objects.filter(constructorid=teamid).aggregate(Sum('laps'))['laps__sum']
    stats['lapsf'] = Results.objects.filter(constructorid=teamid, rank=1).aggregate(Count('raceid'))['raceid__count']
    stats['lapsl'] =  0 # Laptimes.objects.filter(constructorid=teamid, position=1).aggregate(Count('lap'))['lap__count']
    stats['poles'] = Qualifying.objects.filter(constructorid=teamid, position=1).aggregate(Count('position'))['position__count']
    stats['bestq'] = Qualifying.objects.filter(constructorid=teamid).aggregate(Min('position'))['position__min']
    stats['bestr'] = Results.objects.filter(constructorid=teamid).aggregate(Min('position'))['position__min']
    return stats


def getDriverStandings(year):
    with connection.cursor() as cursor:
        cursor.execute('SELECT ds.position, ds.points, d.forename, d.surname, ds.wins, ds.driverId \
                        FROM f1db.driverStandings ds \
                        INNER JOIN f1db.drivers d ON d.driverId = ds.driverId \
                        WHERE ds.raceId = (SELECT MAX(r.raceId) \
                                            FROM f1db.races r \
                                            WHERE EXISTS(SELECT 1 FROM f1db.driverStandings ds WHERE ds.raceId = r.raceId) \
                                            AND r.year = %s) \
                        ORDER BY ds.position', [str(int(year))])
        drivers = cursor.fetchall()
    return drivers


def getConstructorStandings(year):
    with connection.cursor() as cursor:
        cursor.execute('SELECT cs.position, cs.points, c.name, cs.wins, c.constructorId \
                        FROM f1db.constructorStandings cs \
                        INNER JOIN f1db.constructors c ON c.constructorId = cs.constructorId \
                        WHERE cs.raceId = (SELECT MAX(r.raceId) \
                                            FROM f1db.races r \
                                            WHERE EXISTS(SELECT 1 FROM f1db.constructorStandings cs WHERE cs.raceId = r.raceId) \
                                            AND r.year = %s) \
                        ORDER BY cs.position', [str(int(year))])
        drivers = cursor.fetchall()
    return drivers 


def getCircuitResults(circuitid):
    with connection.cursor() as cursor:
        cursor.execute("SELECT r.year, \
                            IFNULL(dq.driverId, -1) AS qid, \
                            IFNULL(dq.forename, '#N/A') AS qfn, \
                            IFNULL(dq.surname, '#N/A') AS qsn, \
                            IFNULL(dr.driverId, -1) AS rid, \
                            IFNULL(dr.forename, '#N/A') AS rfn, \
                            IFNULL(dr.surname, '#N/A') AS rsn \
                        FROM f1db.races r \
                        LEFT JOIN f1db.qualifying q ON q.raceId = r.raceId AND q.position = 1 \
                        LEFT JOIN f1db.drivers dq ON dq.driverId = q.driverId \
                        LEFT JOIN f1db.results res ON res.raceId = r.raceId AND res.position = 1 \
                        LEFT JOIN f1db.drivers dr ON dr.driverId = res.driverId \
                        WHERE r.circuitId = %s \
                        ORDER BY r.year", [str(int(circuitid))])
        drivers = cursor.fetchall()
    return drivers       

