from django.shortcuts import render, redirect
from .models import Job

# Create your views here.
def index(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/index.html', {'jobs': jobs})