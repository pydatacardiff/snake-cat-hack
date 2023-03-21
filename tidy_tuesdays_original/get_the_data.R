# Originally from https://github.com/rfordatascience/tidytuesday/blob/master/data/2023/2023-01-31/readme.md#get-the-data-here
# Get the Data

# Read in with tidytuesdayR package
# Install from CRAN via: install.packages("tidytuesdayR")
# This loads the readme and all the datasets for the week of interest

# Either ISO-8601 date or year/week works!

tuesdata <- tidytuesdayR::tt_load("2023-01-31")
tuesdata <- tidytuesdayR::tt_load(2023, week = 5)

cats_uk <- tuesdata$cats_uk
cats_uk_reference <- tuesdata$cats_uk_reference

# Or read in the data via url and write to disk with pipe
readr::read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-01-31/cats_uk.csv") |>
    readr::write_csv("./tidy_tuesdays_original/cats_uk.csv")
readr::read_csv("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-01-31/cats_uk_reference.csv") |>
    readr::write_csv("./tidy_tuesdays_original/cats_uk_reference.csv")
readr::read_file("https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2023/2023-01-31/readme.md") |>
    readr::write_file("./tidy_tuesdays_original/readme.md")
