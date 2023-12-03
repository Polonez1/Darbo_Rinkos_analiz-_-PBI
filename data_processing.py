import pandas as pd
import json
import config
import numpy as np


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

    def _check_per_hour(self, df: pd.DataFrame):
        condition = df["salary_from"].notna() & df["salary_from"].str.contains("h")
        condition2 = df["salary_to"].notna() & df["salary_to"].str.contains("h")

        df["salary_type"] = np.where(condition, "per hour", df["salary_type"])
        df.loc[condition, "salary_from"] = None

        df["salary_type"] = np.where(condition2, "per hour", df["salary_to"])
        df.loc[condition2, "salary_to"] = None

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
        df = self._check_per_hour(df)

        return df


class ProcessingData:
    cvm = CVmarket()
    cvo = CVonline()

    def processing_cat(self):
        cvmarket_category = self.cvm.category_processing()
        cvonline_category = self.cvo.category_processing()

        return cvmarket_category, cvonline_category

    def processing_main(self):
        cvmarket_data = self.cvm.cvmarket_processing()
        cvonline_data = self.cvo.cvonline_processing()

        # cvmarket = _CVmarket_processing()

        return cvmarket_data, cvonline_data


if "__main__" == __name__:
    cv = ProcessingData()
    df, df2 = cv.processing_main()
    dff = df2.loc[df2["salary_type"].notna() & df2["salary_to"].str.contains("h")]
    print(dff[["salary_to", "salary_type"]])
