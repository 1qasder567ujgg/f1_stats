from django.db import models

class Circuits(models.Model):
    circuitid = models.AutoField(db_column='circuitId', primary_key=True)
    circuitref = models.CharField(db_column='circuitRef', max_length=255)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    alt = models.IntegerField(blank=True, null=True)
    url = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'circuits'


class Constructors(models.Model):
    constructorid = models.AutoField(db_column='constructorId', primary_key=True)
    constructorref = models.CharField(db_column='constructorRef', max_length=255)
    name = models.CharField(unique=True, max_length=255)
    nationality = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'constructors'


class Drivers(models.Model):
    driverid = models.AutoField(db_column='driverId', primary_key=True)
    driverref = models.CharField(db_column='driverRef', max_length=255)
    number = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=3, blank=True, null=True)
    forename = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    dob = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=255, blank=True, null=True)
    url = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'drivers'


class Seasons(models.Model):
    year = models.IntegerField(primary_key=True)
    url = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'seasons'

    def __str__(self):
        return str(self.year)


class Status(models.Model):
    statusid = models.AutoField(db_column='statusId', primary_key=True)
    status = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'status'


class Races(models.Model):
    raceid = models.AutoField(db_column='raceId', primary_key=True)
    year = models.IntegerField()
    round = models.IntegerField()
    circuitid = models.IntegerField(db_column='circuitId')
    name = models.CharField(max_length=255)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    url = models.CharField(unique=True, max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'races'


class ConstructorResults(models.Model):
    constructorresultsid = models.AutoField(db_column='constructorResultsId', primary_key=True)
    raceid = models.ForeignKey(Races, db_column='raceId')
    constructorid = models.ForeignKey(Constructors, db_column='constructorId')
    points = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'constructorResults'


class ConstructorStandings(models.Model):
    constructorstandingsid = models.AutoField(db_column='constructorStandingsId', primary_key=True)
    raceid = models.ForeignKey(Races, db_column='raceId')
    constructorid = models.ForeignKey(Constructors, db_column='constructorId')
    points = models.FloatField()
    position = models.IntegerField(blank=True, null=True)
    positiontext = models.CharField(db_column='positionText', max_length=255, blank=True, null=True)
    wins = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'constructorStandings'


class DriverStandings(models.Model):
    driverstandingsid = models.AutoField(db_column='driverStandingsId', primary_key=True)
    raceid = models.ForeignKey(Races, db_column='raceId')
    driverid = models.ForeignKey(Drivers, db_column='driverId')
    points = models.FloatField()
    position = models.IntegerField(blank=True, null=True)
    positiontext = models.CharField(db_column='positionText', max_length=255, blank=True, null=True)
    wins = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'driverStandings'


class Laptimes(models.Model):
    raceid = models.ForeignKey(Races, db_column='raceId')
    driverid = models.ForeignKey(Drivers, db_column='driverId')
    lap = models.IntegerField()
    position = models.IntegerField(blank=True, null=True)
    time = models.CharField(max_length=255, blank=True, null=True)
    milliseconds = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lapTimes'
        unique_together = (('raceid', 'driverid', 'lap'),)


class Pitstops(models.Model):
    raceid = models.ForeignKey(Races, db_column='raceId')
    driverid = models.ForeignKey(Drivers, db_column='driverId')
    stop = models.IntegerField()
    lap = models.IntegerField()
    time = models.TimeField()
    duration = models.CharField(max_length=255, blank=True, null=True)
    milliseconds = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pitStops'
        unique_together = (('raceid', 'driverid', 'stop'),)


class Qualifying(models.Model):
    qualifyid = models.AutoField(db_column='qualifyId', primary_key=True)
    raceid = models.ForeignKey(Races, db_column='raceId')
    driverid = models.ForeignKey(Drivers, db_column='driverId')
    constructorid = models.ForeignKey(Constructors, db_column='constructorId')
    number = models.IntegerField()
    position = models.IntegerField(blank=True, null=True)
    q1 = models.CharField(max_length=255, blank=True, null=True)
    q2 = models.CharField(max_length=255, blank=True, null=True)
    q3 = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qualifying'


class Results(models.Model):
    resultid = models.AutoField(db_column='resultId', primary_key=True)
    raceid = models.ForeignKey(Races, db_column='raceId')
    driverid = models.ForeignKey(Drivers, db_column='driverId')
    constructorid = models.ForeignKey(Constructors, db_column='constructorId')
    number = models.IntegerField(blank=True, null=True)
    grid = models.IntegerField()
    position = models.IntegerField(blank=True, null=True)
    positiontext = models.CharField(db_column='positionText', max_length=255)
    positionorder = models.IntegerField(db_column='positionOrder')
    points = models.FloatField()
    laps = models.IntegerField()
    time = models.CharField(max_length=255, blank=True, null=True)
    milliseconds = models.IntegerField(blank=True, null=True)
    fastestlap = models.IntegerField(db_column='fastestLap', blank=True, null=True)
    rank = models.IntegerField(blank=True, null=True)
    fastestlaptime = models.CharField(db_column='fastestLapTime', max_length=255, blank=True, null=True)
    fastestlapspeed = models.CharField(db_column='fastestLapSpeed', max_length=255, blank=True, null=True)
    statusid = models.ForeignKey(Status, db_column='statusId')

    class Meta:
        managed = False
        db_table = 'results'


class ConstructorDetail(models.Model):
    constructorid = models.ForeignKey(Constructors)
    # logo
    twitter = models.CharField(max_length=50)
    website = models.CharField(max_length=255)


class DriverDetail(models.Model):
    driverid = models.ForeignKey(Drivers)
    # photo
    twitter = models.CharField(max_length=50)
    website = models.CharField(max_length=255)


class CircuitDetail(models.Model):
    driverid = models.ForeignKey(Circuits)
    # layout
    twitter = models.CharField(max_length=50)
    website = models.CharField(max_length=255)
