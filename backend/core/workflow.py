import datetime
import logging
from threading import Thread

import crawler
from django.db.models import BooleanField, ExpressionWrapper, Q, QuerySet
from core import models
from crawler.workflow import setup_logs
from utils import print_progress_bar


def populate_networks() -> QuerySet[models.Network]:
    logging.info("updating networks")
    bot = crawler.Networks()
    networks = bot.get_networks()
    items = [models.Network(**network.dict()) for network in networks]
    return models.Network.objects.bulk_update_or_create(
        items, ["nome"], match_field="uid"
    )


def populate_network_stations(
    network: models.Network, session=None
) -> list[models.Station]:
    logging.info(f"updating stations for {network}")
    stations = crawler.Stations(session=session, network_uid=network.uid).get_stations()
    uids = [s.uid for s in stations]
    existing_uids = models.Station.objects.filter(uid__in=uids).values_list(
        "uid", flat=True
    )
    new_stations = [
        models.Station(**station.dict(), network=network)
        for station in stations
        if station.uid not in existing_uids
    ]
    return models.Station.objects.bulk_create(new_stations)


def populate_station_parameters(station: models.Station, session=None) -> None:
    logging.info(f"updating parameters for {station}")
    parameters = crawler.Parameters(
        session=session, network_uid=station.network.uid
    ).get_parameters(station_uid=station.uid)
    uids = [p.uid for p in parameters]
    existing_uids = models.Parameter.objects.filter(uid__in=uids).values_list(
        "uid", flat=True
    )
    new_parameters = [
        models.Parameter(**parameter.dict())
        for parameter in parameters
        if parameter.uid not in existing_uids
    ]
    parameters = models.Parameter.objects.bulk_create(new_parameters)
    all_parameters = models.Parameter.objects.filter(uid__in=uids)
    existing_psa_parameters = models.PSA.objects.filter(
        parameter__uid__in=uids, station=station
    ).values_list("parameter", flat=True)
    new_psa = [
        models.PSA(parameter=parameter, station=station)
        for parameter in all_parameters
        if parameter not in existing_psa_parameters
    ]
    models.PSA.objects.bulk_create(new_psa)
    station.last_update = datetime.datetime.now()
    station.save()


def populate_timeseries_data(psa: models.PSA, replace: bool) -> None:
    logging.info(
        f"population data db for parameter {psa.parameter.uid} and station {psa.station.uid} with replace {replace}"
    )

    bot = crawler.GetData()
    now = datetime.datetime.now()
    if replace:
        data = bot.get_data(
            psa.station.uid,
            psa.parameter.uid,
            tmin=datetime.datetime(1930, 1, 1),
            tmax=now,
        )
    else:
        yesterday = now - datetime.timedelta(days=1)
        data = bot.get_data(
            psa.station.uid, psa.parameter.uid, tmin=yesterday, tmax=now
        )

    timestamps = [d.timestamp for d in data.__root__]
    models.Data.objects.filter(psa=psa, timestamp__in=timestamps).delete()
    items = [models.Data(**d.dict(), psa=psa) for d in data.__root__]
    models.Data.objects.bulk_create(items)
    psa.data_last_update = datetime.datetime.now()
    psa.save()


def populate_stations(replace: bool) -> None:
    networks = models.Network.objects.all()
    for index, network in enumerate(networks):
        print_progress_bar(index + 1, networks.count(), prefix="STATIONS")
        if not replace and network.stations.exists():
            continue
        populate_network_stations(network)


def populate_parameters(replace: bool) -> None:
    stations = models.Station.objects.annotate(
        last_update_null=ExpressionWrapper(
            Q(last_update=None), output_field=BooleanField()
        )
    ).order_by("-last_update_null", "last_update")
    for index, station in enumerate(stations):
        print_progress_bar(index + 1, stations.count(), prefix="PARAMETERS")
        if not replace and models.PSA.objects.filter(station=station).exists():
            continue
        populate_station_parameters(station)


def populate_stations_thread() -> None:
    """THIS DOESN'T WORK SOMETIMES - FATAL:  sorry, too many clients already"""
    threads = []
    for network in models.Network.objects.all():
        t = Thread(
            target=populate_network_stations,
            args=(network,),
        )
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


def populate_parameters_thread() -> None:
    """THIS DOESN'T WORK SOMETIMES - FATAL:  sorry, too many clients already"""
    for network in models.Network.objects.all():
        logging.info(f"thread for updating parameters for network {network}")
        threads = []
        for station in network.stations.all():
            t = Thread(
                target=populate_station_parameters,
                args=(station,),
            )
            threads.append(t)
            t.start()
        for t in threads:
            t.join()


def populate_data_thread(replace: bool) -> None:
    """THIS DOESN'T WORK - FATAL:  sorry, too many clients already"""
    for station in models.Station.objects.all():
        psas = models.PSA.objects.filter(station=station)
        threads = []
        for psa in psas:
            t = Thread(
                target=populate_timeseries_data,
                args=(psa, replace),
            )
            threads.append(t)
            t.start()
        for t in threads:
            t.join()


def populate_static_data(replace: bool) -> None:
    setup_logs("static_data")
    populate_networks()
    populate_stations(replace)
    populate_parameters(replace)


def populate_variable_data(replace: bool) -> None:
    setup_logs("timeseries_data")
    psas = models.PSA.objects.annotate(
        last_update_null=ExpressionWrapper(
            Q(data_last_update=None), output_field=BooleanField()
        )
    ).order_by("-last_update_null", "data_last_update")
    for index, psa in enumerate(psas):
        print_progress_bar(index + 1, psas.count(), prefix="DATA")
        populate_timeseries_data(psa, replace)


"""
from core.workflow import *
for s in models.Station.objects.all():
    populate_station_parameters(s)
"""
