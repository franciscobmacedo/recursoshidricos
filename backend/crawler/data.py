import datetime

import pandas as pd
from bs4 import BeautifulSoup
from utils import parse_datetime

from crawler.base import BaseCrawler


class GetData(BaseCrawler):
    def get_data(
        self,
        station_uids: list[str],
        parameter_uids: list[str],
        tmin: datetime.datetime,
        tmax: datetime.datetime,
    ) -> list[dict]:
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
        if df.empty:
            return []
        df_formated = pd.DataFrame()
        date_col = df.columns[0]
        for col in df.columns[1:]:
            df_sp = df.loc[:, [date_col, col]]
            station = df_sp.iloc[0, 1]
            parameter = df_sp.iloc[1, 1]
            try:
                station = Station.objects.get(nome=station.split("(")[0].strip()).uid
            except Station.DoesNotExist:
                pass
            try:
                parameter = Parameter.objects.get(
                    nome=parameter.split("(")[0].strip()
                ).uid
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
        return df_formated.to_dict("records")
