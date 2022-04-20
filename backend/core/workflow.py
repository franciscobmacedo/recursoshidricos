import datetime
import logging
from threading import Thread
from typing import Optional, Literal

import crawler
from django.db.models import BooleanField, ExpressionWrapper, Q, QuerySet
from core import models
from crawler.workflow import setup_logs
from utils import print_progress_bar, date_range


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
    ).get_parameters(station_uids=[station.uid])
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


def get_and_update_timeseries_data(
    psa: models.PSA,
    tmin: datetime.datetime,
    tmax: datetime.datetime,
) -> None:
    bot = crawler.GetData()
    data = bot.get_data(psa.station.uid, psa.parameter.uid, tmin=tmin, tmax=tmax)
    timestamps = [d.timestamp for d in data.__root__]
    logging.debug(f"\n\ndata has {len(timestamps)} entries\n\n")
    if not timestamps:
        return
    models.Data.objects.filter(psa=psa, timestamp__in=timestamps).delete()
    items = [models.Data(**d.dict(), psa=psa) for d in data.__root__]
    models.Data.objects.bulk_create(items)
    psa.data_last_update = datetime.datetime.now()
    psa.save()


def populate_timeseries_data(
    psa: models.PSA,
    replace: bool,
    tmin: Optional[str] = None,
    tmax: Optional[str] = None,
    freq: Optional[Literal["MS", "YS"]] = "YS",
) -> None:
    logging.info(
        f"population data db for parameter {psa.parameter.uid} and station {psa.station.uid} with replace {replace}"
    )

    now = datetime.datetime.now()
    logging.debug("before getting data")

    if tmin:
        tmin = datetime.datetime.strptime(tmin, "%Y-%m-%d")
        tmax = datetime.datetime.strptime(tmax, "%Y-%m-%d") if tmax else now
        d_range = date_range(tmin, tmax, freq)
    elif replace:
        d_range = date_range(datetime.datetime(1930, 1, 1), now, freq)

    else:
        return get_and_update_timeseries_data(
            psa, now - datetime.timedelta(days=1), now
        )

    for dates in d_range:
        get_and_update_timeseries_data(psa, dates[0], dates[1])


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
            if not station.last_update:
                station.last_update = datetime.datetime.now()
                station.save()
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


def populate_variable_data(
    replace: bool,
    network_uid: Optional[str] = None,
    station_uid: Optional[str] = None,
    tmin: Optional[str] = None,
    tmax: Optional[str] = None,
    freq: Optional[Literal["MS", "YS"]] = "YS",
) -> None:
    setup_logs("timeseries_data")

    if station_uid:
        psas = models.PSA.objects.filter(station__uid=station_uid)
    elif network_uid:
        psas = models.PSA.objects.filter(station__network__uid=network_uid)
    else:
        psas = models.PSA.objects.all()

    psas = psas.annotate(
        last_update_null=ExpressionWrapper(
            Q(data_last_update=None), output_field=BooleanField()
        )
    ).order_by("-last_update_null", "data_last_update")
    for index, psa in enumerate(psas):
        logging.debug(f"going to get?, {index}")
        print_progress_bar(index + 1, psas.count(), prefix="DATA")
        try:
            populate_timeseries_data(psa, replace, tmin, tmax, freq)
        except Exception as e:
            logging.error(f"\n\n\nfailed to update data: {e}")


def populate_variable_data_for_parameter(
    parameter: models.Parameter,
) -> None:
    stations = models.Station.objects.filter(psa__parameter=parameter)
    bot = crawler.GetData()

    bot.get_data_and_update_db(
        station_uids=stations.values_list("uid", flat=True),
        parameter_uid=parameter.uid,
        tmin=datetime.datetime(1930, 1, 1),
        tmax=datetime.datetime.now(),
    )


def populate_variable_data_for_all_parameters() -> None:
    setup_logs("timeseries_data")
    parameters = models.Parameter.objects.all()
    for index, parameter in enumerate(parameters):
        logging.debug(f"going to get?, {index}")
        print_progress_bar(index + 1, parameters.count(), prefix="DATA")
        populate_variable_data_for_parameter(parameter)


"""
from core.workflow import *
populate_variable_data_for_parameter(models.Parameter.objects.get(uid="100002982"))
for s in models.Station.objects.all():
    populate_station_parameters(s)
"""
