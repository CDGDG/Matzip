from django.urls import path
from django.contrib.auth import views as auth_views

from user import views

app_name = 'User'

urlpatterns = [
    path("join", views.Join.as_view(), name='join'),
    path("login", auth_views.LoginView.as_view(template_name='user_login.html'), name='login'),
    path("logout", auth_views.LogoutView.as_view(), name='logout'),
]
