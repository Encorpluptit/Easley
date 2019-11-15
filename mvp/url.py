from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .genericsViews import (
    ClientListView,
    ClientDetailView,
    ServiceListView,
    LicenseListView,
    LicenseDetailView,
    ServiceDetailView,
    ServiceUpdateView,
    ClientCreateView,
)
# from . import genericsViews

urlpatterns = [
    path('', views.home, name='mvp-home'),
    path('home/', views.home, name='mvp-home'),
    path('about/', views.about, name='mvp-about'),
    path('contact/', views.contact, name='mvp-contact'),
    path('login/', auth_views.LoginView.as_view(template_name='mvp/login_register/login.html'), name='mvp-login'),
    path('logout/', auth_views.LogoutView.as_view(), name='mvp-logout'),
    path('workspace/', views.workspace, name="mvp-workspace"),
    path('workspace/commercial/', views.commercialWorkspace, name="mvp-commercial-workspace"),
    path('workspace/ceo/', views.ceoWorkspace, name="mvp-ceo-workspace"),
    # path('client/new/', ClientCreateView.as_view(), name='mvp-client-new'),
    path('client/new/', views.clientCreation, name='mvp-client-new'),
    path('client/list/<int:pk>/', ClientListView.as_view(), name='mvp-client-list'),
    path('client/<int:pk>/', ClientDetailView.as_view(), name='mvp-client-details'),
    path('service/new/', views.serviceCreation, name='mvp-service-new'),
    path('service/list/<int:com_pk>/', ServiceListView.as_view(), name='mvp-service-list'),
    path('service/<int:pk>/', ServiceDetailView.as_view(), name='mvp-service-details'),
    path('service/<int:pk>/update', ServiceUpdateView.as_view(), name='mvp-service-update'),
    path('license/new/', views.licenseCreation, name='mvp-license-new'),
    path('license/list/<int:com_pk>/', LicenseListView.as_view(), name='mvp-license-list'),
    path('license/<int:pk>/', LicenseDetailView.as_view(), name='mvp-license-details'),
    path('register/', views.register, name='mvp-register'),
    path('user/update', views.updateUser, name='mvp-profile'),
    path('company/join', views.join_company, name='mvp-join-company'),
    path('company/register', views.companyCreation, name='mvp-company-register'),
]
