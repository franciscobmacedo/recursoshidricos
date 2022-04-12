from django.contrib import admin

from core import models

class NetworkAdmin(admin.ModelAdmin):
    search_fields = ['nome', 'uid']

class StationAdmin(admin.ModelAdmin):
    search_fields = ['nome', 'uid', "codigo"]

class ParameterAdmin(admin.ModelAdmin):
    search_fields = ['nome', 'uid']


class PSAAdmin(admin.ModelAdmin):
    search_fields = ['station__uid', 'parameter__uid', 'station__nome', 'parameter__nome']

admin.site.register(models.Network, NetworkAdmin)
admin.site.register(models.Station, StationAdmin)
admin.site.register(models.Parameter, ParameterAdmin)
admin.site.register(models.Data)
admin.site.register(models.PSA, PSAAdmin)
