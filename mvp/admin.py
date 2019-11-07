from django.contrib import admin
# from .models import Companies, Clients, Service, License, Profile
from .models import Companies, Profile, Clients, License, Service

# Register your models here.
admin.site.register(Profile)
admin.site.register(Companies)
admin.site.register(Clients)
admin.site.register(Service)
admin.site.register(License)
