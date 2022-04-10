from django.contrib import admin

from core import models

# Register your models here.
admin.site.register(models.Network)
admin.site.register(models.Station)
admin.site.register(models.Parameter)
admin.site.register(models.Data)
admin.site.register(models.PSA)
