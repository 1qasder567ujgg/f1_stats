from django.shortcuts import render
from django.http import HttpResponse
from .models import Seasons

# Create your views here.
def main_view(request):
    seasons = Seasons.objects.all().order_by('-year')
    # response_html = '<br>'.join([str(season) for season in seasons])

    return render(request, 'main.html', {'seasons':seasons})