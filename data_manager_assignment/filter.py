import pandas as pd


def subset_variables(dataframe: pd.DataFrame, *variables) -> pd.DataFrame:
    return dataframe[
        [
            *variables
        ]
    ]


def filter_maternal_age_35_and_older(dataframe: pd.DataFrame) -> pd.DataFrame:
    return dataframe[dataframe["maternal_age"] >= 35]
