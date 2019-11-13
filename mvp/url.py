from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='mvp-home'),
    path('home/', views.home, name='mvp-home'),
    path('about/', views.about, name='mvp-about'),
    path('contact/', views.contact, name='mvp-contact'),
    path('login/', auth_views.LoginView.as_view(template_name='mvp/login_register/login.html'), name='mvp-login'),
    path('logout/', auth_views.LogoutView.as_view(), name='mvp-logout'),
    path('workspace/', views.workspace, name="mvp-workspace"),
    path('workspace/commercial', views.commercialWorkspace, name="mvp-commercial-workspace"),
    path('workspace/ceo', views.ceoWorkspace, name="mvp-ceo-workspace"),
    path('client/new', views.clientCreation, name='mvp-client-new'),
    path('register/', views.register, name='mvp-register'),
    path('user/update', views.updateUser, name='mvp-profile'),
    path('company/join', views.join_company, name='mvp-join-company'),
    path('company/register', views.companyCreation, name='mvp-company-register'),
]
