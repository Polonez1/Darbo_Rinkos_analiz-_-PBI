import pandas as pd
import json

import config


def _read_json(json_object: str):
    with open(json_object, "r", encoding="utf-8") as json_file:
        db = json.load(json_file)

    return db


def _get_id_from_url(df: pd.DataFrame) -> pd.DataFrame:
    df["category_id"] = df["url"].str.rpartition("-")[2]
    return df


def _category_processing() -> pd.DataFrame:
    json_obj = _read_json(json_object=config.category_json_path)
    df = pd.DataFrame(json_obj)
    df = _get_id_from_url(df)

    return df


def _CVmarket_processing():
    json_obj = _read_json(json_object=config.CVmarket_json_path)
    df = pd.DataFrame(json_obj)
    df["source"] = "CVMarket"
    df = _get_id_from_url(df)

    return df


def processing_main():
    category = _category_processing()
    cvmarket = _CVmarket_processing()

    return category, cvmarket


if "__main__" == __name__:
    cat, base = processing_main()

    cat.to_excel("category.xlsx")
    base.to_excel("cv_market.xlsx")
