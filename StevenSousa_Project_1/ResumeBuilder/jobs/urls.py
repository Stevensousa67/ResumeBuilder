from django.urls import path
from . import views

app_name = 'jobs'
urlpatterns = [
    path('', views.index, name='index'),
    path('jobs/', views.jobs_list, name='jobs_list'),
]