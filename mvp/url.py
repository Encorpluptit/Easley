from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='mvp-home'),
    path('signin/', views.signin, name='mvp-signin'),
    path('signup/', views.signup, name='mvp-signup'),
]