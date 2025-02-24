from django.urls import path
from . import views

app_name = 'jobs'
urlpatterns = [
    path('', views.index, name='index'),
    path('jobs/', views.jobs_list, name='jobs_list'),
    path('jobs/<str:job_id>/', views.job_details, name='job_details'),
]