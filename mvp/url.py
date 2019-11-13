from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='mvp-home'),
    path('home/', views.home, name='mvp-home'),
    path('about/', views.about, name='mvp-about'),
    path('contact/', views.contact, name='mvp-contact'),
    path('login/', auth_views.LoginView.as_view(template_name='mvp/login.html'), name='mvp-login'),
    path('logout/', auth_views.LogoutView.as_view(), name='mvp-logout'),
    path('register/', views.register, name='mvp-register'),
    path('company/register', views.company_creation, name='mvp-company-register'),
    path('client/register', views.client_creation, name='mvp-client-register')
]
