from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Directories
RAW_PATH = BASE_DIR / "data" / "raw" / "owid_co2.csv"
CLEAN_PATH = BASE_DIR / "data" / "clean" / "emissions_clean.csv"
FIGURES_DIR = BASE_DIR / "outputs" / "figures"
CHANGES_PATH = BASE_DIR / "data" / "clean" / "decoupling_changes.csv"

# Analysis settings
MIN_YEAR = 1990 # Remove any data before this year
BASE_YEAR = 2005 # Start comparison at year 2005
END_YEAR = 2022 # End comparison at this year

# Columns to keep

KEEP_COLUMNS = [
    "country",
    "iso_code",
    "year",
    "population",
    "gdp",
    "co2",
    "co2_per_capita"
]
