from website.models import Seasons
from report.models import Reports

def getSeasons():
    return Seasons.objects.all().order_by('-year')


def getAlphabet():
    return [chr(i) for i in range(65, 91)]


def getYears():
    return [int(year) for year in Seasons.objects.values_list('year', flat=True)].sort()


def getReports():
    return [report for report in Reports.objects.values_list('name', flat=True)]


def getMonacoWeather():
    weather = [
        [2008, 'Гонка после дождя'],
        [2009, 'Изменения в правилах'],
        [2014, 'Изменения в правилах'],
        [2016, 'Дождевая гонка'],
        [2017, 'Изменения в правилах']
    ]
    return weather