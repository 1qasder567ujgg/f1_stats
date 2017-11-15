from django.db import models, connection

from django.db.models import Sum, Count, Min

from website.models import Drivers, Results, Laptimes, Qualifying, Constructors


class SeasonStats(models.Model):

    class Meta:
        managed = False

    def getDriverResults(self, year):
        with connection.cursor() as cursor:
            cursor.execute('SELECT rs.year, d.forename, d.surname, r.driverId \
                            FROM f1db.results r \
                            INNER JOIN f1db.drivers d ON d.driverId = r.driverId \
                            INNER JOIN f1db.races rs ON rs.raceId = r.raceId \
                            WHERE r.constructorId = %s \
                            GROUP BY rs.year, r.driverId, d.forename, d.surname \
                            ORDER BY rs.year, d.surname, d.forename', [str(int(year))])
            row = cursor.fetchall()
        return row  

    def getTeamResults(self, year):
        with connection.cursor() as cursor:
            cursor.execute('SELECT rs.year, d.forename, d.surname, r.driverId \
                            FROM f1db.results r \
                            INNER JOIN f1db.drivers d ON d.driverId = r.driverId \
                            INNER JOIN f1db.races rs ON rs.raceId = r.raceId \
                            WHERE r.year = %s \
                            GROUP BY rs.year, r.driverId, d.forename, d.surname \
                            ORDER BY rs.year, d.surname, d.forename', [str(int(year))])
            row = cursor.fetchall()
        return row  
