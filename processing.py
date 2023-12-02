import pandas as pd
import json
from urllib.parse import urlparse
import config


def _read_json(json_object: str):
    with open(json_object, "r", encoding="utf-8") as json_file:
        db = json.load(json_file)
    return db


class CVmarket:
    cvmarket: str = config.cvmarket_name
    cvmarket_category_file: str = config.category_file.format(name=cvmarket)
    cvmarket_data: str = config.data_file.format(name=cvmarket)

    def _get_id_from_url(self, df: pd.DataFrame) -> pd.DataFrame:
        df["category_id"] = df["url"].str.rpartition("-")[2]
        return df

    def category_processing(self) -> pd.DataFrame:
        json_obj = _read_json(json_object=self.cvmarket_category_file)
        df = pd.DataFrame(json_obj)
        df = self._get_id_from_url(df)

        return df

    def cvmarket_processing(self):
        json_obj = _read_json(json_object=self.cvmarket_data)
        df = pd.DataFrame(json_obj)
        df["source"] = self.cvmarket
        df = self._get_id_from_url(df)

        return df


class CVonline:
    cvonline: str = config.cvonline_name
    cvonline_category_file: str = config.category_file.format(name=cvonline)
    cvonline_data: str = config.data_file.format(name=cvonline)

    def _get_id_from_url(self, df: pd.DataFrame) -> pd.DataFrame:
        df["category_id"] = df["url"].str.rpartition("=")[2]
        return df

    def category_processing(self):
        json_obj = _read_json(json_object=self.cvonline_category_file)
        df = pd.DataFrame(json_obj)
        df = self._get_id_from_url(df)

        return df

    def cvonline_processing(self):
        json_obj = _read_json(json_object=self.cvonline_data)
        df = pd.DataFrame(json_obj)
        df["source"] = self.cvonline
        df = self._get_id_from_url(df)

        return df


def processing_main():
    cvm = CVmarket()
    cvmarket_category = cvm.category_processing()
    cvmarket_data = cvm.cvmarket_processing()

    cvo = CVonline()
    cvonline_category = cvo.category_processing()
    cvonline_data = cvo.cvonline_processing()

    # cvmarket = _CVmarket_processing()

    return cvonline_data


if "__main__" == __name__:
    df = processing_main()
    print(df)
