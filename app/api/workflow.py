from api import crud, get_db


def populate_database(replace):

    print("POPULATING DATABASE")
    from crawler.networks import Networks
    from crawler.parameters import Parameters
    from crawler.stations import Stations

    bot = Networks()
    networks = bot.get()
    crud.create_networks(next(get_db()), networks)
    for network in networks:
        print("getting stations for", network.id)

        stations = Stations(session=bot.session, network_id=network.id).get()
        print("population stations db")
        crud.create_stations(next(get_db()), stations, network_id=network.id)

        for station in stations:
            print("getting parameters for", station.id)
            if not replace:
                if crud.get_stations_parameters(
                    next(get_db()), station_ids=[station.id]
                ):
                    continue

            parameters = Parameters(session=bot.session, network_id=network.id).get(
                station_id=station.id
            )
            print("population parameters db")
            crud.create_parameters(next(get_db()), parameters, station_id=station.id)
