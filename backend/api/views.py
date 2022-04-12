from typing import List

from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from ninja import NinjaAPI, Query, Schema
from ninja.pagination import paginate
from pydantic import Field

from api.filters import DataFilter, Pagination, ParametersFilter, DataBounds
from core import models, schemas

description = """
💧💧💧 access [SNIRH](https://snirh.apambiente.pt/) data  


[source code](https://github.com/franciscobmacedo/recursoshidricos)

"""
api = NinjaAPI(
    title="Recursos Hídricos API",
    description=description,
    version="0.0.1",
)


@api.get("/", include_in_schema=False)
def home(request):
    return redirect("/docs")


@api.get("/networks/", response=List[schemas.Network])
def networks(request):
    return models.Network.objects.all()


@api.get("/networks/{network_uid}", response=schemas.Network)
def network(request, network_uid: str):
    return get_object_or_404(models.Network, uid=network_uid)


@api.get("/stations/", response=List[schemas.Station])
@paginate(Pagination)
def stations(request, network_uid: str):
    return models.Station.objects.filter(network__uid=network_uid)


@api.get("/stations/{station_uid}", response=schemas.Station)
def station(request, station_uid: str):
    return get_object_or_404(models.Station, uid=station_uid)


@api.get("/parameters", response=List[schemas.Parameter])
def parameters(request, filters: ParametersFilter = Query(...)):
    if filters.station_uids:
        psas = models.PSA.objects.filter(station__uid__in=filters.station_uids)
        return models.Parameter.objects.filter(psa__in=psas)

    return models.Parameter.objects.all()


@api.get("/parameters/{parameter_uid}", response=schemas.Parameter)
def parameter(request, parameter_uid: str):
    return get_object_or_404(models.Parameter, uid=parameter_uid)


@api.get("/databounds", response=schemas.DataBounds)
def data_bounds(request, filters: DataBounds = Query(...)):
    psas = models.PSA.objects.filter(
        station__uid__in=filters.station_uids,
        parameter__uid__in=filters.parameter_uids,
    )
    queryset = models.Data.objects.filter(psa__in=psas)
    return schemas.DataBounds(
        tmin=queryset.first().timestamp, tmax=queryset.last().timestamp
    )


@api.get("/data", response=List[schemas.DataReturn])
def data(request, filters: DataFilter = Query(...)):
    psas = models.PSA.objects.filter(
        station__uid__in=filters.station_uids,
        parameter__uid__in=filters.parameter_uids,
    )

    return models.Data.objects.filter(
        psa__in=psas,
        timestamp__gte=filters.tmin,
        timestamp__lte=filters.tmax,
    ).annotate(
        parameter_uid=F("psa__parameter__uid"),
        station_uid=F("psa__station__uid"),
    )
