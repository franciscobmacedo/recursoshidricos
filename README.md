# :sweat_drops: Recursos Hídricos

Transformation of [SNIRH](https://snirh.apambiente.pt/) platform data into an accessible RESTFull API.  
Live at https://api.recursoshidricos.pt/api/v1/

## Table of Contents

- [What is SNIRH?](#what-is-snirh)
- [Motivation](#motivation)
- [Structure](#structure)
- [Setup for development](#setup-for-development)
- [Setup for deployment](#setup-for-deployment)
- [Populate timeseries data](#populate-timeseries-data)
- [Crawler](#crawler)

## What is SNIRH?

[SNIRH](https://snirh.apambiente.pt/) (Sistema Nacional de Informação de Recursos Hídricos - National Information System for Water Resources) is a website built in the mid90s that gives access to all sorts of water resources data accross Portugal. It had little to no updates in the last 30 years.

## Motivation

- The user interface is pretty old and hard to get multiple station's data.
- Provide access to the data in an easy and standard format, through a REST API.
- On top of this API, a frontend modern application can be easily built.

## Structure

This project consists of 4 main containers:

- **backend** - fetches the data and creates a RESTFull API interface for easy access.
- **db** - database container.
- **pgadmin** - admin panel for postgreSQL.
- **frontend** - creates a modern dashboard for easy access. :exclamation: **work in progress** :exclamation:

> :exclamation: **If you only need the crawler (without all this web stuff)** go to [this repo](https://github.com/franciscobmacedo/snirhcrawler)

## Setup for development

build and run for development

```bash
docker-compose up -d --build
```

the api server will be available in http://localhost:8000

You should populate the database with network, stations and parameters data (static data, `-s`):

```bash
docker exec -it backend python3 manage.py populate -s -r # -r stands for replace
```

> :warning: **Fething the data can take a looong time**

## Setup for deployment

1 - Setup traefik - follow this [tutorial](https://www.digitalocean.com/community/tutorials/how-to-use-traefik-v2-as-a-reverse-proxy-for-docker-containers-on-ubuntu-20-04)

2 - edit `docker-compose.prod.yml` traefik domain settings with your domain.

3 - add `.env` file in the main directory (copy from .env.dev)
4 - build and run for production

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

You should populate the database with network, stations and parameters data (static data, `-s`):

```bash
docker exec -it backend python3 manage.py populate -s -r # -r stands for replace
```

> :warning: **Fetching the data can take a looong time**

## Populate timeseries data

<span style="color:red">**Currently, this functionality is ignored, due to long waiting times. The data is directly fetched from SNIRH**</span>

to get all timeseries data and populate the database run:

```bash
docker exec -it backend python3 manage.py populate -t -r # -r stands for replace
```

to get timeseries data just for the last day:

```bash
docker exec -it backend python3 manage.py populate -t
```

> :warning: **Fetching the data can take a looong time**

## Crawler

The crawler accepts multiple commands that will print the data and write it to a `.json` file

> :exclamation: **If you only need the crawler** go to [this repo](https://github.com/franciscobmacedo/snirhcrawler)

```
# all networks
python3 manage.py fetch networks

# all stations for a network_uid
python3 manage.py fetch stations -n {network_uid}

# all params of a station_uid from a network_uid
python3 manage.py fetch params -n {network_uid} -s {station_uid}

# data for a parameter_uid of a station_uid from tmin (yyyy-mm-dd) to tmax (yyyy-mm-dd)
python3 manage.py fetch data -s {station_uid} -p {parameter_uid} -f {tmin} -t {tmax}
```

### Examples

Get all networks - writes it in `data/networks.json`

```
python3 manage.py fetch networks
```

Get all stations of the network 920123705 - writes it in `data/stations-network_920123705.json`

```
python3 manage.py fetch stations -n 920123705
```

Get all parameters of the station 1627758916 inside the network 920123705 - writes it in `data/parameters-station_1627758916.json`

```
python3 manage.py fetch parameters -n 920123705 -s 1627758916
```

Get data for parameter 1849 of the station 1627758916 between 1980-01-01 and 2020-12-31 - writes it in `data/data-station_1627758916-parameter_1849-tmin_1980-01-01-tmax_2020-12-31`

```
python3 manage.py fetch data -s 1627758916 -p 1849 -f 1980-01-01 -t 2020-12-31
```
