from django.shortcuts import render, get_object_or_404
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


def job_details(request, job_id):
    job = get_object_or_404(Job, job_id=job_id)
    context = {
        'job': job,
    }
    return render(request, 'jobs/job_details.html', context)
