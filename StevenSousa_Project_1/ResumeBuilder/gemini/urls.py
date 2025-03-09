from django.urls import path
from . import views

app_name = 'gemini'
urlpatterns = [
    path('generate/<str:job_id>/', views.generate_resume, name='generate_resume'),
    path('resume/<int:pk>/', views.view_resume, name='view_resume'),
    path('resumes/', views.resume_list, name='resume_list'),
    path('generate-cover-letter/<str:job_id>/', views.generate_cover_letter, name='generate_cover_letter'),
    path('cover-letter/<int:pk>/', views.view_cover_letter, name='cover_letter_detail'),
    path('cover-letters/', views.cover_letter_list, name='cover_letter_list'),
]
