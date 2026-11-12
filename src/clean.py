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