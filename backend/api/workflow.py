from api import crud, get_db


def populate_database(replace):

    print("POPULATING DATABASE. REPLACE IS", replace)
    from crawler.networks import Networks
    from crawler.parameters import Parameters
    from crawler.stations import Stations

    bot = Networks()
    networks = bot.get()
    db = next(get_db())
    crud.create_networks(db, networks)
    for network in networks:
        print("getting stations for", network.id)

        stations = Stations(session=bot.session, network_id=network.id).get()
        print("population stations db")
        crud.create_stations(db, stations, network_id=network.id)

        for station in stations:
            if not replace:
                if crud.get_stations_parameters(db, station_ids=[station.id]):
                    continue

            print("getting parameters for", station.id)

            parameters = Parameters(session=bot.session, network_id=network.id).get(
                station_id=station.id
            )
            print("population parameters db")
            crud.create_parameters(db, parameters, station_id=station.id)
