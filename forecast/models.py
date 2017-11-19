from django.db import models

from website.models import Drivers


class Forecast(models.Model):
    driver = models.ForeignKey(Drivers)
    position = models.IntegerField(blank=True, null=True)
    grid = models.IntegerField(blank=True, null=True)