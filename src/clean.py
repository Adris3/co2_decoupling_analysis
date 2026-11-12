import logging
import pandas as pd
from config import (RAW_PATH,
                    CLEAN_PATH,
                    MIN_YEAR,
                    KEEP_COLUMNS,
                    AGGREGATE_PREFIX)

logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(__name__)

def load_raw(path=RAW_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    log.info(f"Loaded raw data: {df.shape[0:,]} rows, {df.shape[1]} columns")
    return df

def drop_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df[df["iso_code"].notna()]
    log.info(f"Dropped {before - len(df):,} non-country rows")
    return df

def filter_years(df: pd.DaraFrame, min_year: int = MIN_YEAR) -> pd.DataFrame:
    before = len(df)
    df = df[df["year"] >= min_year]
    log.info(f"Dropped {before - len(df):,} rows before {min_year}")
    return df

def select_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df[KEEP_COLUMNS].copy()

def handle_missing(df: pd.DataFrame) -> pd.DaraFrame:
    before = len(df)
    df = df.dropna(subset=["population", "gdp", "co2"])
    log.info(f"Dropped {before - len(df):,} rows missing popularion, gdp, or co2")
    return df

def add_features(df: pd.DataFrame) -> None:
    df = df.copy()
    df["gdp_per_capita"] = df["gdp"] / df["population"]
    df["co2_per_gdp"] = df["co2"] / df["gdp"]
    return df

def validate(df: pd.DataFrame) -> None:
    assert not df.duplicated(subset=["iso_code", "year"]).any(), "duplicate country-year rows"
    assert (df["gdp"] > 0).all(), "Non-positive GDP found"
    assert (df["population"] > 0).all(), "Non-positive population found"
    assert (df["co2"] >= 0).all(), "Negative CO2 found"