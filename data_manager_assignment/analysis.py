from collections import Counter
from typing import NoReturn

import pandas as pd
import matplotlib.pyplot as plt


def save_race_ethnicity_vs_preterm_births_frequency_table(dataframe: pd.DataFrame) -> NoReturn:
    preterm_births = dataframe["preterm_births"].apply(lambda x: f"{x} preterm {'birth' if x == '1' else 'births'}")
    frequency_table = pd.crosstab(index=dataframe["m_race_ethnicity"], columns=preterm_births)
    frequency_table.to_csv("data/race_ethnicity_vs_preterm_births_frequency_table.csv")


def save_delivery_method_bar_chart(dataframe: pd.DataFrame) -> NoReturn:
    counter = Counter(dataframe["method_delivery"])
    bars = plt.bar(x=counter.keys(), height=counter.values())

    plt.bar_label(bars)
    plt.title("Deliveries grouped by delivery method")
    plt.xlabel('Delivery method')
    plt.ylabel('Number of deliveries')

    plt.savefig("data/delivery_method_bar_chart.png")
