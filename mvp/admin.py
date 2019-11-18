from django.contrib import admin
from .models import Company, Commercial, Manager, Client, Service, License


# Register your models here.
admin.site.register(Company)
admin.site.register(Manager)
admin.site.register(Commercial)
admin.site.register(Client)
admin.site.register(Service)
admin.site.register(License)
