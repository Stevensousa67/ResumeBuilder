from django.urls import path
from . import views

app_name = 'candidate'
urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('edit/', views.edit_user, name='edit_user'),
    path('profiles/', views.view_profiles, name='view_profiles'),
]
