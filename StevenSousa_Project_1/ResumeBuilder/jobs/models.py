from django.db import models
from django.conf import settings


class Job(models.Model):
    job_id = models.CharField(max_length=500, primary_key=True)
    job_title = models.CharField(max_length=500, blank=False, null=False)
    company_name = models.CharField(max_length=500, blank=False, null=False)
    job_description = models.TextField(blank=False, null=False)
    location = models.CharField(max_length=500, blank=False, null=False)
    min_salary = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    max_salary = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    salary_time = models.CharField(max_length=10, default="yearly")
    posted_date = models.CharField(max_length=500, blank=True, null=True)
    url = models.URLField(max_length=500, blank=False, null=False)
    remote = models.BooleanField(default=False)

    class Meta:
        db_table = 'django_jobs'

    def __str__(self):
        return self.job_title
