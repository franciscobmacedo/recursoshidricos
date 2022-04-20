import datetime

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from utils import parse_datetime

from crawler.base import BaseCrawler
from core.schemas import DataEntryList


def get_field_name(field: str):
    last_par_position = len(field) - field[::-1].index("(") - 1
    return field[:last_par_position].strip()


CHUNK_SIZE = 1000


class GetData(BaseCrawler):
    def get_data(
        self,
        station_uids: list[str],
        parameter_uids: list[str],
        tmin: datetime.datetime,
        tmax: datetime.datetime,
    ) -> DataEntryList:
        from core.models import Station, Parameter

        res = self.get(
            self.data_url,
            params={
                "sites": station_uids,
                "pars": parameter_uids,
                "tmin": tmin.strftime("%d/%m/%Y"),
                "tmax": tmax.strftime("%d/%m/%Y"),
            },
        )
        print(res.url)
        soup = BeautifulSoup(res.text, "html.parser")
        data_table = soup.find_all("table")[-1]
        df = pd.read_html(str(data_table))[0]
        if df.iloc[2:].empty:
            return []
        df_formated = pd.DataFrame()
        date_col = df.columns[0]
        for col in df.columns[1:]:
            df_sp = df.loc[:, [date_col, col]]
            station = df_sp.iloc[0, 1]
            parameter = df_sp.iloc[1, 1]
            try:
                station = Station.objects.get(nome=get_field_name(station)).uid
            except Station.DoesNotExist:
                pass
            try:
                parameter = Parameter.objects.get(nome=get_field_name(parameter)).uid
            except Parameter.DoesNotExist:
                pass
            df_sp["station"] = station
            df_sp["parameter"] = parameter
            df_sp[col] = df_sp[col].replace(r"\s*(.*?)\s*", r"\1", regex=True)
            df_sp.drop(df_sp[df_sp[col] == "-"].index, inplace=True)
            df_sp = df_sp.iloc[2:]
            df_sp.columns = ["timestamp", "value", "station", "parameter"]
            df_formated = pd.concat([df_formated, df_sp])

        df_formated.timestamp = df_formated.timestamp.apply(
            lambda x: parse_datetime(x.strip(), format="%d/%m/%Y %H:%M")
        )
        df_formated.value = df_formated.value.apply(
            lambda x: float(x.strip().split(")")[-1].strip())
        )
        return DataEntryList(__root__=df_formated.to_dict("records"))

    def get_data_and_update_db(
        self,
        station_uids: list[str],
        parameter_uid: str,
        tmin: datetime.datetime,
        tmax: datetime.datetime,
    ) -> None:
        from core import models

        res = self.get(
            self.data_url,
            params={
                "sites": station_uids,
                "pars": parameter_uid,
                "tmin": tmin.strftime("%d/%m/%Y"),
                "tmax": tmax.strftime("%d/%m/%Y"),
            },
        )
        print(res.url)
        soup = BeautifulSoup(res.text, "html.parser")
        data_table = soup.find_all("table")[-1]
        df_total = pd.read_html(str(data_table))[0]
        if df_total.iloc[2:].empty:
            return False
        date_col = df_total.columns[0]
        for col in df_total.columns[1:]:
            df = df_total.loc[:, [date_col, col]]
            print(df)
            station = df.iloc[0, 1]
            station

            station = models.Station.objects.get(nome=get_station_name(df.iloc[0, 1]))
            psa = models.PSA.objects.get(
                station=station,
                parameter__uid=parameter_uid,
            )
            df["psa"] = psa
            df[col] = df[col].replace(r"\s*(.*?)\s*", r"\1", regex=True)
            df.drop(df[df[col] == "-"].index, inplace=True)
            df = df.iloc[2:]
            df.columns = ["timestamp", "value", "psa"]
            df.timestamp = df.timestamp.apply(
                lambda x: parse_datetime(x.strip(), format="%d/%m/%Y %H:%M")
            )
            df.value = df.value.apply(lambda x: float(x.strip().split(")")[-1].strip()))

            for df_chunk in np.array_split(df, CHUNK_SIZE):
                models.Data.objects.filter(
                    psa=psa, timestamp__in=df_chunk.timestamp.tolist()
                ).delete()
                models.Data.objects.bulk_create(
                    models.Data(**vals) for vals in df_chunk.to_dict("records")
                )
