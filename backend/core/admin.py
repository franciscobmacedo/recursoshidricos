from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse

from core import models


class NetworkAdmin(admin.ModelAdmin):
    search_fields = ["nome", "uid"]


class StationAdmin(admin.ModelAdmin):
    search_fields = ["nome", "uid", "codigo"]


class ParameterAdmin(admin.ModelAdmin):
    search_fields = ["nome", "uid"]


class PSAAdmin(admin.ModelAdmin):
    list_display = ("__str__", "station_link", "parameter_link")
    search_fields = [
        "station__uid",
        "parameter__uid",
        "station__nome",
        "parameter__nome",
    ]
    readonly_fields = ("station_link", "parameter_link")

    def station_link(self, obj):
        return mark_safe(
            '<a href="{}">{}</a>'.format(
                reverse("admin:core_station_change", args=(obj.station.pk,)),
                obj.station.__str__(),
            )
        )

    station_link.short_description = "station"

    def parameter_link(self, obj):
        return mark_safe(
            '<a href="{}">{}</a>'.format(
                reverse("admin:core_parameter_change", args=(obj.parameter.pk,)),
                obj.parameter.__str__(),
            )
        )

    parameter_link.short_description = "parameter"


admin.site.register(models.Network, NetworkAdmin)
admin.site.register(models.Station, StationAdmin)
admin.site.register(models.Parameter, ParameterAdmin)
admin.site.register(models.Data)
admin.site.register(models.PSA, PSAAdmin)
