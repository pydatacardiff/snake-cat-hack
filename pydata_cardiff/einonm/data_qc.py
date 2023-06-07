# +
import pandas as pd
import numpy as np
# #!pip install "ydata_profiling"
from ydata_profiling import ProfileReport 

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
# -

# Read in the cats_uk.csv file as a pandas DataFrame, and assign it to the
# variable cats_uk. The index column is the tag_id column, and the data
# types of the columns are specified.

cats_uk = pd.read_csv(
    "../tidy_tuesdays_original/cats_uk.csv",
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
    "../tidy_tuesdays_original/cats_uk_reference.csv",
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

allcat = cats_uk_merged_with_reference.copy()

# Remove the names as data frame index
allcat.reset_index(inplace=True)

# Use a numerical index for the names, and use this index to identify each cat 
names = list(allcat.tag_id.unique())
allcat['name_id'] = allcat.apply(lambda row: names.index(row.tag_id), axis=1)

# datetimearray of timestamp can't be used in a regressor, convert to secs since epoch
allcat['epoch'] = allcat.apply(lambda row: row.timestamp.timestamp(), axis=1)
allcat['epoch'] = allcat['epoch'].astype(int)

# +
# Quick check for bool values stored as strings
for col in allcat:
    if 'TRUE' in allcat[[col]].values:
        print("string bools:", col)

# Which columns have undefined values?
allcat.isna().any()
# -

# hunt has TRUE/FALSE strings - convert to bools
allcat.hunt_fixed = [ x == 'TRUE' for x in allcat.hunt ]

# set gender to one-hot encoding of m/f listing (assumes missing values are female)
allcat.gender = pd.get_dummies(allcat.animal_sex).m

# All these have the same value for all rows - delete!
allcat.drop(['study_name', 'study_site', 'animal_taxon'], axis=1, inplace = True)

# These have been transformed to other columns, so delete
allcat.drop(['tag_id', 'animal_sex'], axis=1, inplace = True)

# These cause issues (missing values/difficult formats), but could be added back in, if of use
allcat.drop(['food_other', 'animal_reproductive_condition', 
             'hunt', 'deploy_on_date', 'deploy_off_date'], axis=1, inplace = True)

# +
# Remove '-Tag' from names
# -

allcat.dropna(inplace=True)

# Only keep entries that have not been flagged as an outlier
allcat = allcat[allcat['algorithm_marked_outlier'] == False]
allcat = allcat[allcat['manually_marked_outlier'] == False]
allcat.drop(['algorithm_marked_outlier', 'manually_marked_outlier'], axis=1, inplace=True)

allcat.head()

allcat.to_csv('cats_uk_qcd.csv', index=False, header=True)

# Produce a profile report 
profile = ProfileReport(allcat)
profile.to_file("cats_uk_profile_report.html")


