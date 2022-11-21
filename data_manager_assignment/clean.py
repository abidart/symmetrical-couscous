from typing import NoReturn
from datetime import datetime

import pandas as pd

from common import DATE_FORMAT

_MIN_MOTHER_YEAR_OF_BIRTH = 1950
_MAX_MOTHER_YEAR_OF_BIRTH = 2010


def remove_unreasonable_birthdates(date_of_birth):
    datetime_date_of_birth = datetime.strptime(date_of_birth, DATE_FORMAT)
    if datetime_date_of_birth.year < _MIN_MOTHER_YEAR_OF_BIRTH \
            or datetime_date_of_birth.year > _MAX_MOTHER_YEAR_OF_BIRTH:
        return pd.NA
    return datetime_date_of_birth.strftime(DATE_FORMAT)


def clean_date_of_birth(dataframe: pd.DataFrame) -> NoReturn:
    dataframe["m_dob"] = dataframe["m_dob"].apply(remove_unreasonable_birthdates)


def clean_birthweight(dataframe: pd.DataFrame) -> NoReturn:
    dataframe["birthweight"] = dataframe["birthweight"].astype("Int64")
    dataframe["birthweight"].replace(to_replace=-99, value=pd.NA, inplace=True)
