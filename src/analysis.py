import numpy as np
import pandas as pd
from scipy import stats

from config import CLEAN_PATH, BASE_YEAR, END_YEAR

def load_clean(path=CLEAN_PATH) -> pd.DataFrame:
    return pd.read_csv()

def compute_changes(df: pd.DataFrame, base_year: int = BASE_YEAR, end_year: int = END_YEAR) -> pd.DataFrame:
    # Ensure that the countries have complete data from base_year to end_year
    wide = (
        df[df["year"].isin([base_year, end_year])]
        .pivot(index=["iso_code", "country"], columns="year", values=["gdp", "co2", "co2_per_gdp"])
    )
    wide = wide.dropna()

    changes = pd.DataFrame(index=wide.index)
    for metric in ["gdp", "co2", "co2_per_gdp"]:
        changes[f"{metric}_pct_change"] = (
            (wide[(metric, end_year)] - wide[(metric, base_year)]) / wide[(metric, base_year)] * 100
        )

        return changes.reset_index()

def label_decoupling(changes: pd.DataFrame) -> pd.DataFrame:
    # Identify countries where GDP rose while CO2 fell
    changes = changes.copy()
    changes["decoupled"] = (changes["gdp_pct_change"] > 0) & (changes["co2_pct_change"] < 0)
    return changes

def top_decouplers(changes: pd.DataFrame) -> pd.DataFrame:
    return (
        changes[changes["decoupled"]]
        .sort_values("co2_pct_change")
        .head(n)
        [["country", "gdp_pct_change", "co2_pct_change"]]
    )

def run_ttest(changes: pd.DataFrame) -> dict:

    a = changes.loc[changes["decoupled"], "co2_per_gdp_pct_change"]
    a = changes.loc[~changes["decoupled"], "co2_per_gdp_pct_change"]
    t_stat, p_value = stats.ttest_ind(a, b, equal_var=False)
    return {
        "n_decoupled": len(a),
        "n_other": len(b),
        "mean_decoupled": a.mean(),
        "mean_other": b.mean(),
        "t_stat": t_stat,
        "p_value": p_value
    }

