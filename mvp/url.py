from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .genericsViews import (
    ClientCreateView,
    ClientUpdateView,
    ClientListView,
    ClientDetailView,
    ClientDeleteView,
    ConseilCreateView,
    ConseilUpdateView,
    ConseilDeleteView,
    LicenseCreateView,
    LicenseUpdateView,
    LicenseDetailView,
    LicenseDeleteView,
    InvoiceCreateView,
    InvoiceUpdateView,
    InvoiceListView,
    InvoiceDetailView,
    InvoiceDeleteView,

    # ConseilDetailView,
    # ContractDetailView,
    # ConseilListView,
    # LicenseListView,
)

urlpatterns = [
    path('', views.home, name='mvp-home'),
    path('home/', views.home, name='mvp-home'),
    path('login/', auth_views.LoginView.as_view(template_name='mvp/misc/login.html'), name='mvp-login'),
    path('logout/', auth_views.LogoutView.as_view(), name='mvp-logout'),
    path('register/', views.register, name='mvp-register'),
    path('company/join', views.join_company, name='mvp-join-company'),
    path('company/register', views.companyCreation, name='mvp-company-register'),
    path('workspace/', views.workspace, name="mvp-workspace"),
    path('workspace/commercial/', views.commercialWorkspace, name="mvp-commercial-workspace"),
    path('workspace/manager/', views.ceoWorkspace, name="mvp-manager-workspace"),
    path('<int:cpny_pk>/contract/new/', views.CreateContractClient, name='mvp-contract-new'),
    path('<int:cpny_pk>/contract/<int:client_pk>/new/', views.CreateContractForm, name='mvp-contract-form'),
    path('<int:cpny_pk>/contract/<int:contract_pk>/details/', views.ContractDetails, name='mvp-contract-details'),
    path('<int:cpny_pk>/contract/<int:contract_pk>/conseil/new/', ConseilCreateView.as_view(), name='mvp-conseil-new'),
    path('<int:cpny_pk>/contract/<int:contract_pk>/conseil/<int:conseil_pk>/details/', views.ConseilDetails, name='mvp-conseil-details'),
    path('<int:cpny_pk>/contract/<int:contract_pk>/conseil/<int:conseil_pk>/update/', ConseilUpdateView.as_view(), name='mvp-conseil-update'),
    path('<int:cpny_pk>/contract/<int:contract_pk>/license/new/', LicenseCreateView.as_view(), name='mvp-license-new'),
    path('<int:cpny_pk>/contract/<int:contract_pk>/license/<int:license_pk>/details/', LicenseDetailView.as_view(), name='mvp-license-details'),
    path('<int:cpny_pk>/contract/<int:contract_pk>/license/update/<int:license_pk>/', LicenseUpdateView.as_view(), name='mvp-license-update'),
    # path('<int:cpny_pk>/contract/<int:contract_pk>/license/update/<int:license_pk>/', views.LicenseUpdate, name='mvp-license-update'),
    # path('<int:cpny_pk>/contract/<int:contract_pk>/details/', ContractDetailView.as_view(), name='mvp-contract-details'),
    # path('<int:cpny_pk>/contract/<int:contract_pk>/conseil/<int:conseil_pk>/details/', ConseilDetailView.as_view(), name='mvp-conseil-details'),
    # path('<int:cpny_pk>/contract/<int:contract_pk>/conseil/<int:conseil_pk>/service/new /', ConseilUpdateView.as_view(), name='mvp-service-new'),










    path('about/', views.about, name='mvp-about'),
    path('contact/', views.contact, name='mvp-contact'),
    # path('client/new/', ClientCreateView.as_view(), name='mvp-client-new'),
    # path('<int:cpny_pk>/client/new', views.clientCreation, name='mvp-client-new'),
    # path('client/new/', views.clientCreation, name='mvp-client-new'),
    # path('service/new/', views.serviceCreation, name='mvp-service-new'),
    # path('service/<int:pk>/update', ConseilUpdateView.as_view(), name='mvp-service-update'),
    # path('license/new/', views.licenseCreation, name='mvp-license-new'),
    path('<int:cpny_pk>/client/new/', ClientCreateView.as_view(), name='mvp-client-new'),
    path('<int:cpny_pk>/client/update/<int:client_pk>/', ClientUpdateView.as_view(), name='mvp-client-update'),
    path('<int:cpny_pk>/client/list/<int:com_pk>/', ClientListView.as_view(), name='mvp-client-list'),
    path('<int:cpny_pk>/client/details/<int:client_pk>/', ClientDetailView.as_view(), name='mvp-client-details'),
    path('<int:cpny_pk>/client/delete/<int:client_pk>/', ClientDeleteView.as_view(), name='mvp-client-delete'),
    # path('<int:cpny_pk>/conseil/new/', ConseilCreateView.as_view(), name='mvp-conseil-new'),
    # path('<int:cpny_pk>/conseil/update/<int:conseil_pk>/', ConseilUpdateView.as_view(), name='mvp-conseil-update'),
    # path('<int:cpny_pk>/conseil/list/<int:com_pk>/', ConseilListView.as_view(), name='mvp-conseil-list'),
    # path('<int:cpny_pk>/conseil/details/<int:conseil_pk>/', ConseilDetailView.as_view(), name='mvp-conseil-details'),
    path('<int:cpny_pk>/conseil/delete/<int:conseil_pk>/', ConseilDeleteView.as_view(), name='mvp-conseil-delete'),
    # path('<int:cpny_pk>/license/new/', LicenseCreateView.as_view(), name='mvp-license-new'),
    # path('<int:cpny_pk>/license/update/<int:license_pk>/', LicenseUpdateView.as_view(), name='mvp-license-update'),
    # path('<int:cpny_pk>/license/list/<int:com_pk>/', LicenseListView.as_view(), name='mvp-license-list'),
    # path('<int:cpny_pk>/license/details/<int:license_pk>/', LicenseDetailView.as_view(), name='mvp-license-details'),
    path('<int:cpny_pk>/license/delete/<int:license_pk>/', LicenseDeleteView.as_view(), name='mvp-license-delete'),
    path('<int:cpny_pk>/invoice/new/', InvoiceCreateView.as_view(), name='mvp-invoice-new'),
    path('<int:cpny_pk>/invoice/update/<int:invoice_pk>', InvoiceUpdateView.as_view(), name='mvp-invoice-update'),
    path('<int:cpny_pk>/invoice/list/', InvoiceListView.as_view(), name='mvp-invoice-list'),
    path('<int:cpny_pk>/invoice/details/<int:invoice_pk>/', InvoiceDetailView.as_view(), name='mvp-invoice-details'),
    path('<int:cpny_pk>/invoice/delete/<int:invoice_pk>/', InvoiceDeleteView.as_view(), name='mvp-invoice-delete'),
    # path('register/', .register, name='mvp-register'),
]
