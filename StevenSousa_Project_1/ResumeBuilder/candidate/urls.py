from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'candidate'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='jobs:index'), name='logout'),
    path('edit_user/', views.edit_user, name='edit_user'),
]
