from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Job

def index(request):
    return render(request, 'jobs/index.html')


def jobs_list(request):
    jobs_listings = Job.objects.all()
    paginator = Paginator(jobs_listings, 25)
    page_number = request.GET.get('page')
    try:
        jobs = paginator.page(page_number)
    except PageNotAnInteger:
        jobs = paginator.page(1)
    except EmptyPage:
        jobs = paginator.page(paginator.num_pages)
    context = {
        'jobs': jobs,
    }

    return render(request, 'jobs/jobs_list.html', context)
