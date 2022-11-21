from typing import NoReturn

import pandas as pd

from clean import clean_birthweight, clean_date_of_birth
from derive_variables import (
    derive_BMI,
    derive_prenatal_visits,
    derive_preterm_births,
    derive_race_ethnicity,
    derive_maternal_age_during_delivery,
    derive_maternal_education_string_format
)
from analysis import save_race_ethnicity_vs_preterm_births_frequency_table, save_delivery_method_bar_chart
from filter import subset_variables, filter_maternal_age_35_and_older

_PATH_TO_INPUT_CSV = "data/mch_dataset.csv"
_PATH_TO_OUTPUT_CSV = "data/subset_data.csv"


def load_dataset(path_to_csv: str) -> pd.DataFrame:
    dataframe = pd.read_csv(path_to_csv)
    return dataframe


def index_data(dataframe: pd.DataFrame):
    assert dataframe["record_ID"].is_unique, "record_ID is not unique"
    dataframe.set_index("record_ID", inplace=True)


def clean_data(dataframe: pd.DataFrame) -> NoReturn:
    clean_date_of_birth(dataframe=dataframe)
    clean_birthweight(dataframe=dataframe)


def derive_new_variables(dataframe: pd.DataFrame) -> NoReturn:
    dataframe["BMI"] = derive_BMI(dataframe=dataframe)
    dataframe["m_race_ethnicity"] = derive_race_ethnicity(dataframe=dataframe)
    dataframe["maternal_age"] = derive_maternal_age_during_delivery(dataframe=dataframe)
    dataframe["number_of_prenatal_visits"] = derive_prenatal_visits(dataframe=dataframe)
    dataframe["preterm_births"] = derive_preterm_births(dataframe=dataframe)
    dataframe["education"] = derive_maternal_education_string_format(dataframe=dataframe)


def analyze_data(dataframe: pd.DataFrame) -> NoReturn:
    save_race_ethnicity_vs_preterm_births_frequency_table(dataframe=dataframe)
    save_delivery_method_bar_chart(dataframe=dataframe)


def filter_data(dataframe: pd.DataFrame) -> NoReturn:
    subset = subset_variables(
        dataframe,
        "m_dob",
        "birthweight",
        "maternal_age",
        "BMI",
        "education",
        "m_race_ethnicity",
        "number_of_prenatal_visits"
    )
    filtered_subset = filter_maternal_age_35_and_older(dataframe=subset)
    return filtered_subset


def save_dataframe(dataframe: pd.DataFrame, output_path: str) -> NoReturn:
    dataframe.to_csv(output_path)


if __name__ == "__main__":
    dataset = load_dataset(path_to_csv=_PATH_TO_INPUT_CSV)
    index_data(dataframe=dataset)
    clean_data(dataframe=dataset)
    derive_new_variables(dataframe=dataset)
    analyze_data(dataframe=dataset)
    subset_dataset = filter_data(dataframe=dataset)
    save_dataframe(dataframe=subset_dataset, output_path=_PATH_TO_OUTPUT_CSV)
