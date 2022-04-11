import datetime
from threading import Thread
import crawler

from core import schemas, models


def populate_networks():
    print("updating networks")
    bot = crawler.Networks()
    networks = bot.get()
    items = [models.Network(**network.dict()) for network in networks]
    return models.Network.objects.bulk_update_or_create(
        items, ["nome"], match_field="uid"
    )


def populate_network_stations(network: models.Network, session=None):
    print(f"updating stations for {network}")
    stations = crawler.Stations(session=session, network_uid=network.uid).get()
    uids = [s.uid for s in stations]
    existing_uids = models.Station.objects.filter(uid__in=uids).values_list(
        "uid", flat=True
    )
    new_stations = [
        models.Station(**station.dict(), network=network)
        for station in stations
        if station.uid not in existing_uids
    ]
    models.Station.objects.bulk_create(new_stations)


def populate_station_parameters(station: models.Station, session=None):
    print(f"updating parameters for {station}")
    parameters = crawler.Parameters(
        session=session, network_uid=station.network.uid
    ).get(station_uid=station.uid)
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


def populate_timeseries_data(psa: models.PSA, replace: bool):
    print(
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
    psa.last_updated = datetime.datetime.now()
    psa.save()


def populate_stations():
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


def populate_parameters():
    for network in models.Network.objects.all():
        print(f"thread for updating parameters for network {network}")
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


def populate_data(replace):
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


def populate_static_data():
    populate_networks()
    populate_stations()
    populate_parameters()


def populate_variable_data(replace):
    for psa in models.PSA.objects.order_by("-last_updated"):
        populate_timeseries_data(psa, replace)


"""
from core.workflow import *
for s in models.Station.objects.all():
    populate_station_parameters(s)
"""
