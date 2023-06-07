import polars as pl

cats_uk = pl.read_csv(
    "tidy_tuesdays_original/cats_uk.csv",
    dtypes={
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

cats_uk.describe()

cats_uk_reference = pl.read_csv(
    "tidy_tuesdays_original/cats_uk_reference.csv",
    dtypes={
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
    null_values=["NA"],
)

cats_uk_reference_with_cats = cats_uk_reference.join(
    cats_uk, on="tag_id", how="left"
).with_columns(
    pl.col(["deploy_on_date", "deploy_off_date", "timestamp"]).str.strptime(
        pl.Datetime, fmt="%+"
    ),
)

cats_uk_reference_with_cats.describe()

# This code groups the data by tag_id, finds the first and last timestamp for each tag_id, and then
# creates a new column that states whether the tag was deployed before, after, or in the time
# period of the data.

cats_uk_reference_with_cats.groupby("tag_id").agg(
    pl.min("timestamp").alias("min_timestamp"),
    pl.max("timestamp").alias("max_timestamp"),
    pl.col("deploy_on_date").first().alias("deploy_on_date"),
    pl.col("deploy_off_date").first().alias("deploy_off_date"),
).select(
    [
        pl.when(pl.col("min_timestamp") < pl.col("deploy_on_date"))
        .then("before")
        .when(pl.col("max_timestamp") > pl.col("deploy_off_date"))
        .then("after")
        .otherwise("in")
        .alias("deploy_status")
    ]
).filter(
    pl.col("deploy_status") != "in"
)

# This code takes the cats_uk_reference_with_cats dataset and groups it by tag_id.
# It then finds the earliest timestamp for each tag_id and the latest timestamp for each tag_id.
# It then subtracts the earliest timestamp from the latest timestamp to find the duration of the tag_id.
# It then returns the tag_id, the earliest timestamp, the latest timestamp, and the duration.

duration_per_cat = (
    cats_uk_reference_with_cats.groupby("tag_id")
    .agg(
        pl.min("timestamp").alias("min_timestamp"),
        pl.max("timestamp").alias("max_timestamp"),
    )
    .with_columns(
        (pl.col("max_timestamp") - pl.col("min_timestamp").alias("duration")).alias(
            "duration"
        ),
    )
)

# Plot the duration of each tag_id as a histogram
import plotly_express as px

# plot duration as histogram
px.histogram(x=duration_per_cat.select("duration").to_series()).show()

events_per_cat = cats_uk_reference_with_cats.groupby("tag_id").agg(
    pl.count("event_id").alias("event_count")
)

# Plot the number of events per tag_id as a histogram
px.histogram(x=events_per_cat.select("event_count").to_series()).show()


def lag(name: str, n: int) -> pl.Expr:
    return pl.col(name) - pl.col(name).shift(n)


lag_timestamp = lag("timestamp", 1).alias("interval")

# This code takes the cats_uk_reference_with_cats dataset and groups it by tag_id.
# It then finds the lag of the timestamp for each tag_id.
# It then returns the tag_id and the lag of the timestamp.

interval_per_event = (
    cats_uk_reference_with_cats.select("tag_id", "timestamp")
    .sort("timestamp")
    .groupby("tag_id")
    .agg(
        lag_timestamp,
    )
    .explode("interval")
    .with_columns(pl.col("interval").cast(pl.Utf8).alias("interval_string"))
)

# plot duration as histogram
px.histogram(x=interval_per_event.select("interval").to_series(), nbins=20).show()
