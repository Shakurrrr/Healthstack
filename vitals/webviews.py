from django.shortcuts import render
from .models import Athlete

def dashboard(request):
    athletes = Athlete.objects.all().order_by("name")
    return render(request, "vitals/dashboard.html", {"athletes": athletes})