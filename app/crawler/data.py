import datetime

import pandas as pd
from bs4 import BeautifulSoup
from common.schemas import DataEntryList
from common.utils import parse_datetime

from crawler.base import BaseCrawler


class GetData(BaseCrawler):
    def get_data(
        self,
        station_id: str,
        parameter_id: str,
        tmin: datetime.datetime,
        tmax: datetime.datetime,
    ) -> DataEntryList:
        res = self.session.get(
            self.data_url,
            params={
                "sites": station_id,
                "pars": parameter_id,
                "tmin": tmin.strftime("%d/%m/%Y"),
                "tmax": tmax.strftime("%d/%m/%Y"),
            },
        )
        soup = BeautifulSoup(res.text, "html.parser")
        data_table = soup.find_all("table")[-1]
        df = pd.read_html(str(data_table))[0]
        df = df.iloc[2:]
        print(df)
        if df.empty:
            return DataEntryList(__root__=[])

        df.columns = ["timestamp", "value"]
        df.timestamp = df.timestamp.apply(
            lambda x: parse_datetime(x.strip(), format="%d/%m/%Y %H:%M")
        )
        df.value = df.value.apply(lambda x: float(x.strip().split(")")[-1].strip()))
        return DataEntryList(__root__=df.to_dict("records"))
