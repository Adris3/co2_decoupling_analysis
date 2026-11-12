import pandas as pd
import pytest

from config import CLEAN_PATH


@pytest.fixture(scope="module")
def clean_df():
    return pd.read_csv(CLEAN_PATH)


def test_no_duplicate_country_year(clean_df):
    dupes = clean_df.duplicated(subset=["iso_code", "year"]).sum()
    assert dupes == 0, f"Found {dupes} duplicate country-year rows"


def test_gdp_positive(clean_df):
    assert (clean_df["gdp"] > 0).all(), "Found non-positive GDP values"


def test_population_positive(clean_df):
    assert (clean_df["population"] > 0).all(), "Found non-positive population values"


def test_co2_non_negative(clean_df):
    assert (clean_df["co2"] >= 0).all(), "Found negative CO2 values"


def test_expected_columns_present(clean_df):
    expected = {"country", "iso_code", "year", "population", "gdp", "co2", "co2_per_capita"}
    assert expected.issubset(clean_df.columns), f"Missing columns: {expected - set(clean_df.columns)}"


def test_iso_codes_are_three_letters(clean_df):
    assert clean_df["iso_code"].str.len().eq(3).all(), "Found iso_code not 3 characters long"


def test_year_range(clean_df):
    assert clean_df["year"].min() >= 1990, "Found years before 1990"
    assert clean_df["year"].max() <= 2025, "Found implausible future years"


def test_reasonable_row_count(clean_df):
    assert len(clean_df) > 1000, "Unexpectedly few rows after cleaning"