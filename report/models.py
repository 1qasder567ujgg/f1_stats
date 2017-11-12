from django.db import models

# from website.models import Constructors, Drivers, Races, ConstructorStandings, DriverStandings

# class CurrentDriverPoints(models.Model):
#     lastRace = Races.objects.all().order_by('-date')[0]
#     driverPoints = DriverStandings.objects.all().filter(raceid=lastRace).order_by('-points')[:11]


# SELECT 
#     ds.`position`,
#     d.`forename`,
#     d.`surname`,
#     ds.`points`,
#     ds.`wins`
# FROM
#     f1db.driverStandings ds
#         INNER JOIN
#     f1db.drivers d ON d.driverId = ds.driverId
# WHERE
#     ds.raceId = (SELECT 
#             MAX(dm.raceId)
#         FROM
#             f1db.driverStandings dm)
# ORDER BY ds.position
# LIMIT 10;
