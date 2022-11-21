from typing import Iterable, NoReturn
from datetime import datetime

import pandas as pd
from pandas._libs.missing import NAType

from common import DATE_FORMAT

_MATERNAL_EDUCATION_MAP = {
    1: "Less than High School",
    2: "High School",
    3: "Some College",
    4: "College",
    5: "Professional degree",
    -99: "Missing"
}


def calculate_variable_with_map(dataset: pd.DataFrame, function: callable, columns_for_map=Iterable[str]) -> pd.Series:
    iterables = [dataset[column] for column in columns_for_map]
    return pd.Series(
        data=map(function, *iterables),
        index=dataset.index
    )


def calculate_BMI(weight_lb: int, height_in: int) -> float:
    return round(weight_lb / height_in ** 2 * 703, 2)


def derive_BMI(dataframe: pd.DataFrame) -> pd.Series:
    return calculate_variable_with_map(
        dataset=dataframe,
        function=calculate_BMI,
        columns_for_map=("m_weight_lb", "m_height_in")
    )


def calculate_race_ethnicity(race: str, ethnicity: str) -> str:
    if ethnicity == "Hispanic":
        return "Hispanic"
    if race in ("White", "Black"):
        return f"Non-Hispanic {race}"
    return "Non-Hispanic Other"


def derive_race_ethnicity(dataframe: pd.DataFrame) -> pd.Series:
    return calculate_variable_with_map(
        dataset=dataframe,
        function=calculate_race_ethnicity,
        columns_for_map=("m_race", "m_ethnicity")
    )


def calculate_maternal_age_during_delivery(date_of_birth: str, date_of_delivery: str) -> int | NAType:
    if type(date_of_birth) != str:
        return pd.NA
    datetime_dob = datetime.strptime(date_of_birth, DATE_FORMAT)
    datetime_delivery = datetime.strptime(date_of_delivery, DATE_FORMAT)
    birthday_has_passed = (datetime_delivery.month, datetime_delivery.day) >= (datetime_dob.month, datetime_dob.day)
    difference_in_years = datetime_delivery.year - datetime_dob.year
    return difference_in_years if birthday_has_passed else difference_in_years - 1


def derive_maternal_age_during_delivery(dataframe: pd.DataFrame) -> pd.Series:
    return calculate_variable_with_map(
        dataset=dataframe,
        function=calculate_maternal_age_during_delivery,
        columns_for_map=("m_dob", "date_of_delivery")
    )


def calculate_prenatal_visits(*prenatal_visit) -> int:
    return sum([type(visit) != float for visit in prenatal_visit])


def derive_prenatal_visits(dataframe: pd.DataFrame) -> pd.Series:
    return calculate_variable_with_map(
        dataset=dataframe,
        function=calculate_prenatal_visits,
        columns_for_map=(
            "prenatal_vis1",
            "prenatal_vis2",
            "prenatal_vis3",
            "prenatal_vis4",
            "prenatal_vis5",
            "prenatal_vis6",
            "prenatal_vis7",
            "prenatal_vis8",
            "prenatal_vis9",
            "prenatal_vis10",
            "prenatal_vis11"
        )
    )


def calculate_preterm_births(gptal: int) -> str:
    return str(gptal)[2]


def derive_preterm_births(dataframe: pd.DataFrame) -> pd.Series:
    return calculate_variable_with_map(
        dataset=dataframe,
        function=calculate_preterm_births,
        columns_for_map=("GPTAL",)
    )


def convert_numerical_maternal_education_to_string(education_level: int) -> str:
    return _MATERNAL_EDUCATION_MAP[education_level]


def derive_maternal_education_string_format(dataframe: pd.DataFrame) -> pd.Series:
    return calculate_variable_with_map(
        dataset=dataframe,
        function=convert_numerical_maternal_education_to_string,
        columns_for_map=("m_edu",)
    )
