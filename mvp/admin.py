from django.contrib import admin
from .models import Company, Client, License, Service, Ceo, Commercial

# Register your models here.
# admin.site.register(Profile)
admin.site.register(Company)
admin.site.register(Ceo)
admin.site.register(Commercial)
admin.site.register(Client)
admin.site.register(Service)
admin.site.register(License)
