# # Some machine learning
#
# WIP. Do a quick regression trying to predict the age of a cat

# +
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
# -

# Read in the cats_uk QC'd data set

allcat = pd.read_csv(
    "../cats_uk_qcd.csv",
)

# Remove text based columns we can't regress on
allcat.drop(['timestamp', 'animal_id'], axis=1, inplace=True)

# +
X = allcat.copy()
y = X.pop('age_years')

# Test/train split, taking age as the dependent variable
train_X, val_X, train_y, val_y = train_test_split(X, y)

model = RandomForestRegressor()
y = allcat.age_years.dropna()
# -

dummy = model.fit(train_X, train_y)

val_predictions = dtr_model.predict(val_X)

print(mean_absolute_error(val_y, val_predictions))
