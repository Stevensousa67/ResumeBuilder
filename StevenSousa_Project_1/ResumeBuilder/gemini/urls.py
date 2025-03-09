from django.urls import path
from . import views

app_name = 'gemini'
urlpatterns = [
    path('generate/<str:job_id>/', views.generate_resume, name='generate_resume'),
    path('resume/<int:pk>/', views.view_resume, name='view_resume'),
    path('resumes/', views.resume_list, name='resume_list'),
]