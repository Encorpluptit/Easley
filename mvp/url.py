from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='mvp-home'),
    path('home/', views.home, name='mvp-home'),
    path('login/', auth_views.LoginView.as_view(template_name='mvp/login.html'), name='mvp-login'),
    # path('login/', views.login, name='mvp-login'),
    path('register/', views.register, name='mvp-register'),
]
