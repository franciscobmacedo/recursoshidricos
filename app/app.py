from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app import crud, get_db
from common import schemas
from crawler.data import GetData

from common.utils import parse_datetime

description = """
💧💧💧 access [SNIRH](https://snirh.apambiente.pt/) data  


[source code](https://github.com/franciscobmacedo/snirhAPI)

"""

app = FastAPI(
    title="snirhAPI",
    description=description,
    version="0.0.1",
)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/redoc")


@app.get("/networks/", response_model=List[schemas.Network])
async def networks(db: Session = Depends(get_db)):
    networks = crud.get_networks(db)
    return networks


@app.get("/networks/{network_id}", response_model=schemas.Network)
async def network(network_id: str, db: Session = Depends(get_db)):
    network = crud.get_network(db, network_id)
    if not network:
        raise HTTPException(status_code=404, detail=f"Network {network_id} not found")
    return network


@app.get("/stations/", response_model=List[schemas.Station])
async def stations(network_id: str, db: Session = Depends(get_db)):
    stations = crud.get_network_stations(db, network_id=network_id)
    return stations


@app.get("/stations/{station_id}", response_model=schemas.Station)
async def station(station_id: str, db: Session = Depends(get_db)):
    station = crud.get_station(db, station_id=station_id)
    if not station:
        raise HTTPException(status_code=404, detail=f"Station {station_id} not found")
    return station


@app.get(
    "/parameters",
    response_model=List[schemas.Parameter],
)
async def parameters(station_ids: Optional[str] = None, db: Session = Depends(get_db)):
    if station_ids:
        _station_ids = station_ids.split(",")
        parameters = crud.get_stations_parameters(db, station_ids=_station_ids)
    else:
        parameters = crud.get_parameters(db)

    if not parameters:
        raise HTTPException(status_code=404, detail=f"Parameters not found")
    return parameters


@app.get("/parameters/{parameter_id}", response_model=schemas.Parameter)
async def parameter(parameter_id: str, db: Session = Depends(get_db)):
    parameter = crud.get_parameter(db, parameter_id=parameter_id)
    if not parameter:
        raise HTTPException(
            status_code=404, detail=f"parameter {parameter_id} not found"
        )

    parameter.dict()
    return parameter


@app.get("/data/")
async def data(
    station_id: str,
    parameter_id: str,
    tmin: str = "1980-01-01",
    tmax: str = "2020-12-31",
) -> schemas.DataEntryList:
    bot = GetData()
    return bot.get_data(
        station_id=station_id,
        parameter_id=parameter_id,
        tmin=parse_datetime(tmin, format="%Y-%m-%d"),
        tmax=parse_datetime(tmax, format="%Y-%m-%d"),
    )
