import datetime
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema, Query
from core import schemas, models
from typing import List
from pydantic import Field
from django.db.models import F
from django.shortcuts import redirect


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
def add(request):
    return redirect("/docs")


@api.get("/networks/", response=List[schemas.Network])
def networks(request):
    return models.Network.objects.all()


@api.get("/networks/{network_uid}", response=schemas.Network)
def network(request, network_uid: str):
    return get_object_or_404(models.Network, uid=network_uid)


@api.get("/stations/", response=List[schemas.Station])
def stations(request, network_uid: str):
    return models.Station.objects.filter(network__uid=network_uid)


@api.get("/stations/{station_uid}", response=schemas.Station)
def station(request, station_uid: str):
    return get_object_or_404(models.Station, uid=station_uid)


class ParametersFilter(Schema):
    station_uids: List[str] = Field(None, alias="station_uids")


@api.get("/parameters", response=List[schemas.Parameter])
def parameters(request, filters: ParametersFilter = Query(...)):
    if filters.station_uids:
        psas = models.PSA.objects.filter(station__uid__in=filters.station_uids)
        return models.Parameter.objects.filter(psa__in=psas)

    return models.Parameter.objects.all()


@api.get("/parameters/{parameter_uid}", response=schemas.Parameter)
def parameter(request, parameter_uid: str):
    return get_object_or_404(models.Parameter, uid=parameter_uid)


class DataFilter(Schema):
    station_uids: List[str]
    parameter_uids: List[str]
    tmin: datetime.date
    tmax: datetime.date


@api.get("/data", response=schemas.DataReturnList)
def data(request, filters: DataFilter = Query(...)):
    print("here", filters)
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
    # return models.Parameter.objects.first()


# @app.get("/parameters/{parameter_id}", response_model=schemas.Parameter)
# async def parameter(parameter_id: str, db: Session = Depends(get_db)):
#     parameter = crud.get_parameter(db, parameter_id=parameter_id)
#     if not parameter:
#         raise HTTPException(
#             status_code=404, detail=f"parameter {parameter_id} not found"
#         )

#     parameter.dict()
#     return parameter


# @app.get("/data/")
# async def data(
#     station_id: str,
#     parameter_id: str,
#     db: Session = Depends(get_db),
# ):
#     # return crud.get_station_parameter(db, station_id, parameter_id)

#     from api.workflow import populate_timeseries_data

#     # populate_timeseries_data(station_id, parameter_id, True)
#     data = crud.get_data(db, station_id=station_id, parameter_id=parameter_id)
#     print(data)
#     return data
#     # bot = GetData()
#     # d = bot.gg(
#     #     station_ids=station_ids,
#     #     parameter_ids=parameter_ids,
#     #     tmin=parse_datetime(tmin, format="%Y-%m-%d"),
#     #     tmax=parse_datetime(tmax, format="%Y-%m-%d"),
#     # )
#     # return d
