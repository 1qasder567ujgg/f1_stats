from django.db import models

# from django.db.models import Sum, Count, Min

# from website.models import Drivers, Results, Laptimes, Qualifying, Constructors


class Reports(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=255, blank=True, null=True)
    methodname = models.CharField(max_length=50)
