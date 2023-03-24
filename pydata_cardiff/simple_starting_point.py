import pandas as pd

# Read in the cats_uk.csv file as a pandas DataFrame, and assign it to the
# variable cats_uk. The index column is the tag_id column, and the data
# types of the columns are specified.

cats_uk = pd.read_csv(
    "tidy_tuesdays_original/cats_uk.csv",
    index_col="tag_id",
    parse_dates=["timestamp"],
    dtype={
        "tag_id": str,
        "event_id": str,
        "visible": bool,
        "location_long": float,
        "location_lat": float,
        "ground_speed": int,
        "height_above_ellipsoid": float,
        "algorithm_marked_outlier": bool,
        "manually_marked_outlier": bool,
        "study_name": str,
    },
)

cats_uk.head()

cats_uk.info()

# Read in the cats_uk_reference.csv file as a pandas DataFrame, and assign it
# to the variable cats_uk_reference. The index column is the tag_id column,
# the deploy_on_date and deploy_off_date columns are parsed as dates, and
# the data types of the columns are specified.

cats_uk_reference = pd.read_csv(
    "tidy_tuesdays_original/cats_uk_reference.csv",
    index_col="tag_id",
    parse_dates=["deploy_on_date", "deploy_off_date"],
    dtype={
        "tag_id": str,
        "animal_id": str,
        "animal_taxon": str,
        "hunt": str,
        "prey_p_month": float,
        "animal_reproductive_condition": str,
        "animal_sex": str,
        "hrs_indoors": float,
        "n_cats": int,
        "food_dry": bool,
        "food_wet": bool,
        "food_other": str,
        "study_site": str,
        "age_years": float,
    },
)

cats_uk_reference.head()

cats_uk_reference.info()

# Merge the cats_uk and cats_uk_reference DataFrames on the tag_id index
# into a new DataFrame. This DataFrame duplicates the information in the
# cats_uk_reference DataFrame for each tag_id as the relationship is many-to-one.

cats_uk_merged_with_reference = pd.merge(cats_uk, cats_uk_reference, on="tag_id")

len(cats_uk_merged_with_reference) == len(cats_uk)

len(cats_uk_merged_with_reference) == len(cats_uk_reference)
