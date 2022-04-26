from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Query
from ninja.pagination import paginate

from api.filters import DataFilter, Pagination, ParametersFilter
from core.schemas import DataEntryList
from crawler.data import GetData
from utils import parse_datetime
from core import models, schemas


description = """
💧💧💧 access [SNIRH](https://snirh.apambiente.pt/) data  


[source code](https://github.com/franciscobmacedo/recursoshidricos)

"""
api = NinjaAPI(
    title="Recursos Hídricos API",
    description=description,
    version="1.0.0",
    docs_url="/",
)

from ninja import Router

networks_router = Router()
stations_router = Router()
parameters_router = Router()
data_router = Router()


@networks_router.get(
    "/",
    response=list[schemas.Network],
    description="get all networks",
)
def networks(request):
    return models.Network.objects.all()


@networks_router.get(
    "/{network_uid}",
    response=schemas.Network,
    description="get one network",
)
def network(request, network_uid: str):
    return get_object_or_404(models.Network, uid=network_uid)


@stations_router.get(
    "/",
    response=list[schemas.Station],
    description="get stations that belong to a network",
)
@paginate(Pagination)
def stations(request, network_uid: str):
    return models.Station.objects.filter(network__uid=network_uid)


@stations_router.get(
    "/{station_uid}", response=schemas.Station, description="get one station"
)
def station(request, station_uid: str):
    return get_object_or_404(models.Station, uid=station_uid)


@parameters_router.get(
    "/",
    response=list[schemas.Parameter],
    description="get all parameters or filter by one or more stations",
)
def parameters(request, filters: ParametersFilter = Query(...)):
    if filters.station_uids:
        psas = models.PSA.objects.filter(station__uid__in=filters.station_uids)
        print(psas)
        return models.Parameter.objects.filter(psa__in=psas)

    return models.Parameter.objects.all()


@parameters_router.get(
    "/{parameter_uid}", response=schemas.Parameter, description="get one parameter"
)
def parameter(request, parameter_uid: str):
    return get_object_or_404(models.Parameter, uid=parameter_uid)


@data_router.get(
    "/",
    response=DataEntryList,
    description="",
)
def data(request, filters: DataFilter = Query(...)):
    """
    Get timeseries data for one or more stations and one or more parameters between two dates.
    You need to provide:
    - **station_uids**: uid(s) of one or more station
    - **parameters_uids**: uid(s) of one or more parameter
    - **tmin**: start date in yyyy-mm-dd format
    - **tmax**: end date in yyyy-mm-dd format
    """
    bot = GetData()
    return bot.get_data(
        filters.station_uids,
        filters.parameter_uids,
        tmin=filters.tmin,
        tmax=filters.tmax,
    )


# @data_router.get(
#     "/",
#     response=list[schemas.DataReturn],
#     description="",
# )
# def data(request, filters: DataFilter = Query(...)):
#     """
#     Get timeseries data for one or more stations and one or more parameters between two dates.
#     You need to provide:
#     - **station_uids**: uid of each station
#     - **parameters_uids**: uid of each parameter
#     - **tmin**: start date in yyyy-mm-dd format
#     - **tmax**: end date in yyyy-mm-dd format
#     """
#     psas = models.PSA.objects.filter(
#         station__uid__in=filters.station_uids,
#         parameter__uid__in=filters.parameter_uids,
#     )

#     return models.Data.objects.filter(
#         psa__in=psas,
#         timestamp__gte=filters.tmin,
#         timestamp__lte=filters.tmax,
#     ).annotate(
#         parameter_uid=F("psa__parameter__uid"),
#         station_uid=F("psa__station__uid"),
#     )


# @data_router.get(
#     "/bounds",
#     response=Optional[schemas.DataBounds],
#     description="get min and max dates of the available timeseries data for one or more stations and one or more parameters",
# )
# def data_bounds(request, filters: DataBounds = Query(...)):
#     psas = models.PSA.objects.filter(
#         station__uid__in=filters.station_uids,
#         parameter__uid__in=filters.parameter_uids,
#     )
#     queryset: QuerySet[models.Data] = models.Data.objects.filter(psa__in=psas).order_by(
#         "timestamp"
#     )
#     if queryset.exists():
#         return schemas.DataBounds(
#             tmin=queryset.first().timestamp, tmax=queryset.last().timestamp
#         )
#     return None


api.add_router("/networks/", networks_router, tags=["networks"])
api.add_router("/stations/", stations_router, tags=["stations"])
api.add_router("/parameters/", parameters_router, tags=["parameters"])
api.add_router("/data/", data_router, tags=["data"])
