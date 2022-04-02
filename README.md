# :sweat_drops: SNIRH API

Transformation of [SNIRH](https://snirh.apambiente.pt/) platform data into an accessible RESTFull API.

running at https://snirhapi.herokuapp.com/

## What is SNIRH?

[SNIRH](https://snirh.apambiente.pt/) (Sistema Nacional de Informação de Recursos Hídricos - National Information System for Water Resources) is a website built in the mid90s that gives access to all sorts of water resources data accross Portugal. It had little to no updates in the last 30 years.

## Motivation

- The user interface is pretty old and hard to get multiple station's data.
- Provide access to the data in an easy and standard format, through a REST API.
- On top of this API, a frontend modern application can be easily built.

## Development

This project consists of 2 main blocks:

- [**Crawler**](crawler) - fetches the data and transforms it into standart python formats.
- [**App**](app) - uses the fetched data and creates a RESTFull API interface for easy access.

### Setup in your local machine

_WINDOWS_

```bash
git clone https://github.com/franciscobmacedo/snirhAPI
cd  snirhAPI
py -m venv venv
.\venv\scripts\activate
pip install -r requirements.txt # requirements/dev.txt for development or requirements/common.txt for just the crawler
```

_MAC/LINUX_

```bash
git clone https://github.com/franciscobmacedo/snirhAPI
cd  snirhAPI
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt # requirements/dev.txt for development or requirements/common.txt for just the crawler
```

### run the app

```
python3 run.py app
```

### run the crawler

The crawler accepts multiple commands that will print the data and write it to a `.json` file

```
# all networks
python3 run.py crawler networks

# all stations for a network_id
python3 run.py crawler stations -n {network_id}

# all params of a station_id from a network_id
python3 run.py crawler params -n {network_id} -s {station_id}

# data for a parameter_id of a station_id from tmin (yyyy-mm-dd) to tmax (yyyy-mm-dd)
python3 run.py crawler data -s {station_id} -p {parameter_id} -f {tmin} -t {tmax}
```

#### Examples

Get all networks - writes it in `data/networks.json`

```
python3 run.py crawler networks
```

Get all stations of the network 920123705 - writes it in `data/stations-network_920123705.json`

```
python3 run.py crawler stations -n 920123705
```

Get all parameters of the station 1627758916 inside the network 920123705 - writes it in `data/parameters-station_1627758916.json`

```
python3 run.py crawler parameters -n 920123705 -s 1627758916
```

Get data for parameter 1849 of the station 1627758916 between 1980-01-01 and 2020-12-31 - writes it in `data/data-station_1627758916-parameter_1849-tmin_1980-01-01-tmax_2020-12-31`

```
python3 run.py crawler data -s 1627758916 -p 1849 -f 1980-01-01 -t 2020-12-31
```
