from django.contrib import admin
from .models import Job

# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('job_id', 'job_title', 'company_name', 'location', 'min_salary','max_salary', 'salary_time',
                    'posted_date', 'url', 'remote')
