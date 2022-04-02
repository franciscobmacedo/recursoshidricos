from typing import Optional

from sqlalchemy.orm import Session

from app import models
from common import schemas


def get_networks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Network).offset(skip).limit(limit).all()


def get_network(db: Session, network_id: str):
    try:
        return db.query(models.Network).filter(models.Network.id == network_id).first()
    except:
        return None


def create_networks(db: Session, networks: list[schemas.Network]):
    objects = [
        models.Network(**network.dict())
        for network in networks
        if not get_network(db, network.id)
    ]
    db.bulk_save_objects(objects)
    db.commit()


def get_network_stations(db: Session, network_id: str):
    try:
        return (
            db.query(models.Station)
            .filter(models.Station.network_id == network_id)
            .all()
        )
    except:
        return None


def get_station(db: Session, station_id: str):
    try:
        return db.query(models.Station).filter(models.Station.id == station_id).first()
    except:
        return None


def create_stations(db: Session, stations: list[schemas.Station], network_id: str):
    objects = [
        models.Station(**station.dict(), network_id=network_id)
        for station in stations
        if not get_station(db, station.id)
    ]
    db.bulk_save_objects(objects)
    db.commit()


def get_parameter(db: Session, parameter_id: str):
    try:
        return (
            db.query(models.Parameter)
            .filter(models.Parameter.id == parameter_id)
            .first()
        )
    except:
        return None


def get_parameters(db: Session, skip: int = 0, limit: int = 1000):
    try:
        return db.query(models.Parameter).offset(skip).limit(limit).all()
    except:
        return None


def get_stations_parameters(db: Session, station_ids: Optional[list[str]]):
    try:

        return (
            db.query(models.Parameter)
            .filter(models.Parameter.stations.any(models.Station.id.in_(station_ids)))
            .all()
        )
    except:
        return None


def create_parameters(
    db: Session, parameters: list[schemas.Parameter], station_id: str
):
    station = get_station(db, station_id)
    for parameter in parameters:
        if not (object := get_parameter(db, parameter.id)):
            object = models.Parameter(**parameter.dict())
            db.add(object)
            db.commit()
        if station not in object.stations:
            object.stations = object.stations + [station]
