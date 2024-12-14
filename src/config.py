# src/config.py

from pathlib import Path

FILEPATH = Path("data/daily-rainfall-at-30-sites-1960-to-2022.csv")

DEFAULT_DATA = {

    "SITE" : "Whangārei (Northland)",

    "YEAR" : 2022,

    "WIDTH_ROOF_M" : 12,
    "LENGTH_ROOF_M" : 32,

    "DIAM_INT_TANK_M" : 4,
    "HEIGHT_INT_TANK_M"  : 5,

    "NUMBER_USERS" : 7,
    "VOLUME_PER_DAY_PER_PERSON_L" : 150

}